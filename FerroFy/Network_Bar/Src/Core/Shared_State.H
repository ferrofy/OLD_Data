#pragma once
#include <atomic>
#include <cstdint>

struct Net_Stats {
    std::atomic<double>   Upload_Bps   { 0.0 };
    std::atomic<double>   Download_Bps { 0.0 };
    std::atomic<uint64_t> Total_Sent   { 0 };
    std::atomic<uint64_t> Total_Recv   { 0 };
    std::atomic<uint32_t> Ping_Ms      { 0 };
    std::atomic<bool>     Is_Online    { false };
    std::atomic<uint64_t> Packets_Sent { 0 };
    std::atomic<uint64_t> Packets_Recv { 0 };
};

struct App_State {
    std::atomic<bool> Running        { true };
    std::atomic<bool> Overlay_Visible{ true };
    std::atomic<bool> Startup_Enabled{ false };
    std::atomic<bool> Draggable      { false };
    std::atomic<int>  Overlay_X      { 12 };
    std::atomic<int>  Overlay_Y      { 12 };
};

inline Net_Stats  G_Net_Stats;
inline App_State  G_App_State;
