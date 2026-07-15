#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <iphlpapi.h>
#include <icmpapi.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <cstdint>
#include <cstring>
#include "../Core/App_Config.H"
#include "../Core/Shared_State.H"
#include "Net_Monitor.H"

#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")

static HANDLE    G_Net_Thread   = nullptr;
static HANDLE    G_Ping_Thread  = nullptr;

static DWORD Find_Best_Interface_Index()
{
    PMIB_IFTABLE If_Table = nullptr;
    DWORD        Buf_Len  = 0;
    DWORD        Ret;

    Ret = GetIfTable(If_Table, &Buf_Len, FALSE);
    if (Ret != ERROR_INSUFFICIENT_BUFFER) return 0;

    If_Table = (PMIB_IFTABLE)malloc(Buf_Len);
    if (!If_Table) return 0;

    Ret = GetIfTable(If_Table, &Buf_Len, FALSE);
    if (Ret != NO_ERROR) { free(If_Table); return 0; }

    DWORD Best_Idx   = 0;
    ULONG64 Best_Vol = 0;

    for (DWORD i = 0; i < If_Table->dwNumEntries; i++) {
        MIB_IFROW& Row = If_Table->table[i];
        if (Row.dwType == IF_TYPE_SOFTWARE_LOOPBACK) continue;
        if (Row.dwOperStatus != IF_OPER_STATUS_OPERATIONAL &&
            Row.dwOperStatus != IF_OPER_STATUS_CONNECTED)   continue;

        ULONG64 Vol = (ULONG64)Row.dwInOctets + (ULONG64)Row.dwOutOctets;
        if (Vol > Best_Vol) {
            Best_Vol = Vol;
            Best_Idx = Row.dwIndex;
        }
    }

    free(If_Table);
    return Best_Idx;
}

static DWORD WINAPI Ping_Thread_Func(LPVOID)
{
    HANDLE Icmp = IcmpCreateFile();
    if (Icmp == INVALID_HANDLE_VALUE) return 0;

    const char Payload[] = "NB";
    const DWORD Reply_Size = sizeof(ICMP_ECHO_REPLY) + sizeof(Payload) + 8;
    BYTE  Reply_Buf[sizeof(ICMP_ECHO_REPLY) + 64];

    IPAddr Target = inet_addr("8.8.8.8");

    while (G_App_State.Running.load(std::memory_order_relaxed)) {
        DWORD Ret = IcmpSendEcho(
            Icmp,
            Target,
            (LPVOID)Payload, (WORD)sizeof(Payload),
            nullptr,
            Reply_Buf, Reply_Size,
            PING_TIMEOUT_MS
        );

        if (Ret > 0) {
            ICMP_ECHO_REPLY* Reply = (ICMP_ECHO_REPLY*)Reply_Buf;
            if (Reply->Status == IP_SUCCESS) {
                G_Net_Stats.Ping_Ms.store((uint32_t)Reply->RoundTripTime, std::memory_order_relaxed);
                G_Net_Stats.Is_Online.store(true, std::memory_order_relaxed);
            } else {
                G_Net_Stats.Ping_Ms.store(0, std::memory_order_relaxed);
                G_Net_Stats.Is_Online.store(false, std::memory_order_relaxed);
            }
        } else {
            G_Net_Stats.Is_Online.store(false, std::memory_order_relaxed);
        }

        for (int i = 0; i < (PING_INTERVAL_MS / 100) && G_App_State.Running.load(std::memory_order_relaxed); i++) {
            Sleep(100);
        }
    }

    IcmpCloseHandle(Icmp);
    return 0;
}

DWORD WINAPI Net_Monitor_Thread(LPVOID)
{
    LARGE_INTEGER Freq, T_Prev, T_Now;
    QueryPerformanceFrequency(&Freq);
    QueryPerformanceCounter(&T_Prev);

    MIB_IFROW Row_Prev = {};
    bool      First    = true;
    int       Refresh_Count = 0;
    DWORD     Best_Idx = 0;

    while (G_App_State.Running.load(std::memory_order_relaxed)) {
        Refresh_Count++;
        if (Refresh_Count >= 20 || Best_Idx == 0) {
            Best_Idx = Find_Best_Interface_Index();
            Refresh_Count = 0;
        }

        if (Best_Idx == 0) {
            Sleep(NET_POLL_MS);
            continue;
        }

        MIB_IFROW Row_Now = {};
        Row_Now.dwIndex   = Best_Idx;
        if (GetIfEntry(&Row_Now) != NO_ERROR) {
            Sleep(NET_POLL_MS);
            continue;
        }

        QueryPerformanceCounter(&T_Now);
        double Delta_Sec = (double)(T_Now.QuadPart - T_Prev.QuadPart) / (double)Freq.QuadPart;

        if (!First && Delta_Sec > 0.01) {
            DWORD Raw_Up  = Row_Now.dwOutOctets - Row_Prev.dwOutOctets;
            DWORD Raw_Dn  = Row_Now.dwInOctets  - Row_Prev.dwInOctets;

            double Upload   = (double)Raw_Up  / Delta_Sec;
            double Download = (double)Raw_Dn  / Delta_Sec;

            G_Net_Stats.Upload_Bps.store(Upload,   std::memory_order_relaxed);
            G_Net_Stats.Download_Bps.store(Download, std::memory_order_relaxed);

            uint64_t Sent_Total = G_Net_Stats.Total_Sent.load(std::memory_order_relaxed) + Raw_Up;
            uint64_t Recv_Total = G_Net_Stats.Total_Recv.load(std::memory_order_relaxed) + Raw_Dn;
            G_Net_Stats.Total_Sent.store(Sent_Total, std::memory_order_relaxed);
            G_Net_Stats.Total_Recv.store(Recv_Total, std::memory_order_relaxed);

            G_Net_Stats.Packets_Sent.store((uint64_t)Row_Now.dwOutUcastPkts + Row_Now.dwOutNUcastPkts, std::memory_order_relaxed);
            G_Net_Stats.Packets_Recv.store((uint64_t)Row_Now.dwInUcastPkts  + Row_Now.dwInNUcastPkts,  std::memory_order_relaxed);
        }

        Row_Prev = Row_Now;
        T_Prev   = T_Now;
        First    = false;

        Sleep(NET_POLL_MS);
    }
    return 0;
}

bool Net_Monitor_Start()
{
    WSADATA Wsa;
    WSAStartup(MAKEWORD(2, 2), &Wsa);

    G_Net_Thread = CreateThread(nullptr, 0, Net_Monitor_Thread, nullptr, 0, nullptr);
    if (!G_Net_Thread) return false;
    SetThreadPriority(G_Net_Thread, THREAD_PRIORITY_BELOW_NORMAL);

    G_Ping_Thread = CreateThread(nullptr, 0, Ping_Thread_Func, nullptr, 0, nullptr);
    if (!G_Ping_Thread) return false;
    SetThreadPriority(G_Ping_Thread, THREAD_PRIORITY_LOWEST);

    return true;
}

void Net_Monitor_Stop()
{
    if (G_Net_Thread) {
        WaitForSingleObject(G_Net_Thread, 2000);
        CloseHandle(G_Net_Thread);
        G_Net_Thread = nullptr;
    }
    if (G_Ping_Thread) {
        WaitForSingleObject(G_Ping_Thread, 2000);
        CloseHandle(G_Ping_Thread);
        G_Ping_Thread = nullptr;
    }
    WSACleanup();
}
