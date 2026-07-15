#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#define SLEEP_MS(x) Sleep(x)
#else
#include <unistd.h>
#define SLEEP_MS(x) usleep((x)*1000)
#endif

#define RED  "\033[91m"
#define GRN  "\033[92m"
#define YLW  "\033[93m"
#define CYN  "\033[96m"
#define MGT  "\033[95m"
#define WHT  "\033[97m"
#define GRY  "\033[90m"
#define BLD  "\033[1m"
#define RST  "\033[0m"
#define BLU  "\033[94m"

#define MAX          64
#define JSON_PATH    "Data/Users.json"

typedef struct {
    int   Id;
    char  Land_Id[20];
    char  Owner[60];
    char  Location[80];
    float Area;
    float Price;
    char  Type[16];
    char  Status[16];
    char  Prev_Hash[12];
    char  Hash[12];
    long  Timestamp;
} Block;

Block Chain[MAX];
int   Count = 0;

void Enable_Colors(void) {
#ifdef _WIN32
    HANDLE H = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD  M = 0;
    GetConsoleMode(H, &M);
    SetConsoleMode(H, M | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
    SetConsoleOutputCP(CP_UTF8);
#endif
}

void Make_Hash(Block *B) {
    unsigned long H = 5381;
    char Buf[256];
    snprintf(Buf, sizeof(Buf), "%d%s%s%.0f%ld", B->Id, B->Land_Id, B->Owner, B->Price, B->Timestamp);
    for (int I = 0; Buf[I]; I++) H = H * 33 ^ (unsigned char)Buf[I];
    snprintf(B->Hash, sizeof(B->Hash), "%08lx", H & 0xFFFFFFFF);
}

void Add_Block(const char *Land_Id, const char *Owner, const char *Loc,
               float Area, float Price, const char *Type, const char *Status) {
    if (Count >= MAX) return;
    Block *B   = &Chain[Count];
    B->Id        = Count;
    B->Timestamp = (long)time(NULL);
    B->Area      = Area;
    B->Price     = Price;
    snprintf(B->Land_Id,  sizeof(B->Land_Id),  "%s", Land_Id);
    snprintf(B->Owner,    sizeof(B->Owner),     "%s", Owner);
    snprintf(B->Location, sizeof(B->Location),  "%s", Loc);
    snprintf(B->Type,     sizeof(B->Type),      "%s", Type);
    snprintf(B->Status,   sizeof(B->Status),    "%s", Status);
    if (Count == 0) {
        snprintf(B->Prev_Hash, sizeof(B->Prev_Hash), "00000000");
    } else {
        char Tmp[12];
        memcpy(Tmp, Chain[Count-1].Hash, sizeof(Tmp));
        snprintf(B->Prev_Hash, sizeof(B->Prev_Hash), "%s", Tmp);
    }
    Make_Hash(B);
    Count++;
}

void Spinner(const char *Msg) {
    const char *F[] = {"|", "/", "-", "\\"};
    for (int I = 0; I < 12; I++) {
        printf(CYN "\r  %s  " WHT "%s" RST "   ", F[I%4], Msg);
        fflush(stdout);
        SLEEP_MS(60);
    }
    printf(GRN "\r  [+] " WHT "%s" RST "   \n", Msg);
}

void Banner(void) {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
    printf(CYN BLD);
    printf("\n  +===============================================================+\n");
    printf("  |" YLW BLD "   BLOCKCHAIN LAND REGISTRY  ~  DEMO SYSTEM                " CYN BLD "|\n");
    printf("  |" GRY "   Immutable  |  Transparent  |  Tamper-Proof               " CYN BLD "|\n");
    printf("  +===============================================================+\n");
    printf(RST "\n");
}

void Line_Thick(void) {
    printf(CYN "  +---------------------------------------------------------------+\n" RST);
}

void Line_Thin(void) {
    printf(GRY "  |---------------------------------------------------------------|\n" RST);
}

void Folder_Row(const char *Label, const char *Color, const char *Value) {
    printf(GRY "  | " RST GRY "%-14s" RST ": %s%-44s" RST GRY " |\n" RST, Label, Color, Value);
}

void Folder_Row_F(const char *Label, float Value, const char *Suffix) {
    char Buf[48];
    snprintf(Buf, sizeof(Buf), "%.0f %s", Value, Suffix);
    Folder_Row(Label, WHT, Buf);
}

void Print_Block_Folder(Block *B) {
    const char *S_Col = GRN;
    if (strcmp(B->Status, "DISPUTED")    == 0) S_Col = RED;
    if (strcmp(B->Status, "TRANSFERRED") == 0) S_Col = YLW;

    char Block_Title[48];
    snprintf(Block_Title, sizeof(Block_Title), " BLOCK #%d  [ %s ]", B->Id, B->Land_Id);

    printf("\n");
    printf(MGT BLD "  +-- " YLW "%-52s" MGT " ---+\n" RST, Block_Title);
    printf(MGT "  |" RST GRY "                                                               " MGT "|\n" RST);
    Folder_Row("Owner",     WHT BLD, B->Owner);
    Folder_Row("Location",  WHT,     B->Location);
    Folder_Row_F("Area",    B->Area, "sqft");
    {
        char Price_Buf[48];
        snprintf(Price_Buf, sizeof(Price_Buf), "INR %.0f", B->Price);
        Folder_Row("Price", GRN, Price_Buf);
    }
    Folder_Row("Tx Type",   CYN,     B->Type);
    Folder_Row("Status",    S_Col,   B->Status);
    {
        char Time_Buf[32];
        time_t T = (time_t)B->Timestamp;
        struct tm *TM = localtime(&T);
        strftime(Time_Buf, sizeof(Time_Buf), "%Y-%m-%d %H:%M:%S", TM);
        Folder_Row("Timestamp", GRY, Time_Buf);
    }
    printf(GRY "  |                                                               |\n" RST);
    Line_Thin();
    printf(GRY "  | " RST MGT "Prev Hash" RST GRY "  : " MGT "%-44s" GRY " |\n" RST, B->Prev_Hash);
    printf(GRY "  | " RST MGT BLD "Hash      " RST GRY ": " MGT BLD "%-44s" GRY " |\n" RST, B->Hash);
    printf(MGT BLD "  +---------------------------------------------------------------+\n" RST);
}

void View_All_Table(void) {
    printf(CYN BLD "\n  %-12s %-22s %-22s %-10s %s\n" RST,
           "Land ID", "Owner", "Location", "Area(sqft)", "Status");
    printf(GRY "  %-12s %-22s %-22s %-10s %s\n" RST,
           "--------", "-----", "--------", "----------", "------");
    for (int I = 0; I < Count; I++) {
        Block *B = &Chain[I];
        if (strcmp(B->Type, "GENESIS") == 0) continue;
        const char *C = GRN;
        if (strcmp(B->Status, "DISPUTED")    == 0) C = RED;
        if (strcmp(B->Status, "TRANSFERRED") == 0) C = YLW;
        printf("  " WHT "%-12s %-22s %-22s %-10.0f %s%s\n" RST,
               B->Land_Id, B->Owner, B->Location, B->Area, C, B->Status);
    }
    printf(GRY "\n  Total Records: " YLW BLD "%d\n\n" RST, Count - 1);
}

void Verify(void) {
    Spinner("Verifying Chain Integrity");
    int OK = 1;
    for (int I = 1; I < Count; I++) {
        if (strcmp(Chain[I].Prev_Hash, Chain[I-1].Hash) != 0) {
            printf(RED BLD "  [!] CHAIN BROKEN At Block #%d!\n" RST, I);
            OK = 0;
        }
    }
    char Old[12];
    for (int I = 0; I < Count; I++) {
        snprintf(Old, sizeof(Old), "%s", Chain[I].Hash);
        Make_Hash(&Chain[I]);
        if (strcmp(Old, Chain[I].Hash) != 0) {
            printf(RED BLD "  [!] HASH MISMATCH At Block #%d — Tampered!\n" RST, I);
            OK = 0;
        }
    }
    if (OK) printf(GRN BLD "\n  [+] ALL %d BLOCKS VALID — Chain Is Intact!\n\n" RST, Count);
}

void Input_Str(const char *P, char *Buf, int N) {
    printf(CYN "  >> " WHT "%s" RST ": ", P);
    fflush(stdout);
    if (fgets(Buf, N, stdin)) {
        int L = (int)strlen(Buf);
        if (L > 0 && Buf[L-1] == '\n') Buf[L-1] = '\0';
    }
}

float Input_Float(const char *P) {
    char B[32]; Input_Str(P, B, sizeof(B)); return (float)atof(B);
}

int Input_Int(const char *P) {
    char B[16]; Input_Str(P, B, sizeof(B)); return atoi(B);
}

void Pause(void) {
    printf(GRY "\n  Press ENTER To Continue..." RST);
    fflush(stdout);
    while (getchar() != '\n');
}

int Find_Land(const char *Id) {
    for (int I = Count-1; I >= 0; I--)
        if (strcmp(Chain[I].Land_Id, Id) == 0) return I;
    return -1;
}

static char *Json_Str(const char *Src, char *Field, char *Out, int Max) {
    char Key[64];
    snprintf(Key, sizeof(Key), "\"%s\"", Field);
    char *P = strstr(Src, Key);
    if (!P) { Out[0] = '\0'; return NULL; }
    P += strlen(Key);
    while (*P == ' ' || *P == ':' || *P == ' ') P++;
    if (*P == '"') {
        P++;
        int I = 0;
        while (*P && *P != '"' && I < Max-1) Out[I++] = *P++;
        Out[I] = '\0';
    }
    return P;
}

static float Json_Float(const char *Src, const char *Field) {
    char Key[64];
    snprintf(Key, sizeof(Key), "\"%s\"", Field);
    char *P = strstr(Src, Key);
    if (!P) return 0.0f;
    P += strlen(Key);
    while (*P == ' ' || *P == ':') P++;
    return (float)atof(P);
}

void Load_Json(void) {
    FILE *F = fopen(JSON_PATH, "r");
    if (!F) return;

    fseek(F, 0, SEEK_END);
    long Sz = ftell(F);
    rewind(F);
    char *Buf = (char *)malloc(Sz + 1);
    if (!Buf) { fclose(F); return; }
    fread(Buf, 1, Sz, F);
    Buf[Sz] = '\0';
    fclose(F);

    char *Cur = Buf;
    while ((Cur = strchr(Cur, '{')) != NULL) {
        char *End = strchr(Cur, '}');
        if (!End) break;
        int Len = (int)(End - Cur) + 1;
        char *Obj = (char *)malloc(Len + 1);
        if (!Obj) break;
        strncpy(Obj, Cur, Len);
        Obj[Len] = '\0';

        char Land_Id[20], Owner[60], Loc[80], Type[16], Status[16];
        Json_Str(Obj, "Land_Id",  Land_Id, sizeof(Land_Id));
        Json_Str(Obj, "Owner",    Owner,   sizeof(Owner));
        Json_Str(Obj, "Location", Loc,     sizeof(Loc));
        Json_Str(Obj, "Type",     Type,    sizeof(Type));
        Json_Str(Obj, "Status",   Status,  sizeof(Status));
        float Area  = Json_Float(Obj, "Area");
        float Price = Json_Float(Obj, "Price");

        if (Land_Id[0] != '\0' && Owner[0] != '\0')
            Add_Block(Land_Id, Owner, Loc, Area, Price, Type, Status);

        free(Obj);
        Cur = End + 1;
    }
    free(Buf);
}

void Save_Json(void) {
    FILE *F = fopen(JSON_PATH, "w");
    if (!F) { printf(RED "  [!] Cannot Write To %s\n" RST, JSON_PATH); return; }

    fprintf(F, "{\n  \"Records\": [\n");
    int First = 1;
    for (int I = 0; I < Count; I++) {
        Block *B = &Chain[I];
        if (strcmp(B->Type, "GENESIS") == 0) continue;
        if (!First) fprintf(F, ",\n");
        First = 0;
        fprintf(F,
            "    {\n"
            "      \"Land_Id\":  \"%s\",\n"
            "      \"Owner\":    \"%s\",\n"
            "      \"Location\": \"%s\",\n"
            "      \"Area\":     %.0f,\n"
            "      \"Price\":    %.0f,\n"
            "      \"Type\":     \"%s\",\n"
            "      \"Status\":   \"%s\"\n"
            "    }",
            B->Land_Id, B->Owner, B->Location,
            B->Area, B->Price, B->Type, B->Status);
    }
    fprintf(F, "\n  ]\n}\n");
    fclose(F);
}

int main(void) {
    Enable_Colors();

    Add_Block("GENESIS", "System", "Origin", 0, 0, "GENESIS", "ACTIVE");
    Load_Json();

    int Run = 1;
    while (Run) {
        Banner();
        printf(CYN BLD "  +---------------------------+\n");
        printf("  |       MAIN  MENU          |\n");
        printf("  +---------------------------+\n" RST);
        printf("  " GRN "[ 1 ]" WHT "  View All Records\n" RST);
        printf("  " YLW "[ 2 ]" WHT "  Register New Land\n" RST);
        printf("  " YLW "[ 3 ]" WHT "  Transfer Ownership\n" RST);
        printf("  " CYN "[ 4 ]" WHT "  Search By Land ID\n" RST);
        printf("  " MGT "[ 5 ]" WHT "  View Block Folders\n" RST);
        printf("  " GRN "[ 6 ]" WHT "  Verify Chain Integrity\n" RST);
        printf("  " RED "[ 0 ]" WHT "  Exit\n" RST);
        printf(GRY "\n  Chain Blocks : " YLW BLD "%d\n\n" RST, Count);

        int C = Input_Int("Select Option");
        printf("\n");

        if (C == 1) {
            printf(CYN BLD "\n  === ALL LAND RECORDS ===\n" RST);
            View_All_Table();
            Pause();
        }
        else if (C == 2) {
            printf(CYN BLD "\n  === REGISTER NEW LAND ===\n\n" RST);
            char Id[20], Own[60], Loc[80];
            Input_Str("Land ID (e.g. LND-005)", Id, sizeof(Id));
            if (Find_Land(Id) >= 0) {
                printf(RED "  [!] Land ID Already Registered!\n" RST);
                Pause(); continue;
            }
            Input_Str("Owner Name", Own, sizeof(Own));
            Input_Str("Location",   Loc, sizeof(Loc));
            float A = Input_Float("Area In Sqft");
            float P = Input_Float("Price In INR");
            Spinner("Adding Block To Blockchain");
            Add_Block(Id, Own, Loc, A, P, "REGISTER", "ACTIVE");
            Save_Json();
            printf(GRN "  [+] Land Registered! Block #%d Added & Saved To JSON.\n" RST, Count-1);
            Pause();
        }
        else if (C == 3) {
            printf(CYN BLD "\n  === TRANSFER OWNERSHIP ===\n\n" RST);
            char Id[20], New_Own[60];
            Input_Str("Land ID To Transfer", Id, sizeof(Id));
            int Idx = Find_Land(Id);
            if (Idx < 0) { printf(RED "  [!] Land ID Not Found!\n" RST); Pause(); continue; }
            printf(GRY "  Current Owner : " WHT BLD "%s\n" RST, Chain[Idx].Owner);
            Input_Str("New Owner Name", New_Own, sizeof(New_Own));
            Spinner("Sealing Transfer Block Into Chain");
            Add_Block(Id, New_Own, Chain[Idx].Location, Chain[Idx].Area, Chain[Idx].Price, "TRANSFER", "TRANSFERRED");
            Save_Json();
            printf(GRN "  [+] Ownership Transferred! Block #%d Added & Saved To JSON.\n" RST, Count-1);
            Pause();
        }
        else if (C == 4) {
            printf(CYN BLD "\n  === SEARCH BY LAND ID ===\n\n" RST);
            char Id[20]; Input_Str("Enter Land ID", Id, sizeof(Id));
            int Found = 0;
            for (int I = 0; I < Count; I++)
                if (strcmp(Chain[I].Land_Id, Id) == 0) { Print_Block_Folder(&Chain[I]); Found++; }
            if (!Found) printf(YLW "\n  [~] No Records Found.\n" RST);
            Pause();
        }
        else if (C == 5) {
            printf(CYN BLD "\n  === BLOCK FOLDERS ===\n" RST);
            printf(GRY "  Range: 0 To %d\n" RST, Count-1);
            printf(GRY "  (Enter -1 To View All Blocks)\n\n" RST);
            int Idx = Input_Int("Block Index (-1 = All)");
            if (Idx == -1) {
                for (int I = 0; I < Count; I++) Print_Block_Folder(&Chain[I]);
            } else if (Idx >= 0 && Idx < Count) {
                Print_Block_Folder(&Chain[Idx]);
            } else {
                printf(RED "  [!] Out Of Range.\n" RST);
            }
            Pause();
        }
        else if (C == 6) {
            printf(CYN BLD "\n  === CHAIN INTEGRITY CHECK ===\n\n" RST);
            Verify();
            Pause();
        }
        else if (C == 0) {
            Spinner("Exiting System");
            printf(GRN "  [+] Goodbye!\n\n" RST);
            Run = 0;
        }
        else {
            printf(RED "  [!] Invalid Option.\n" RST);
            Pause();
        }
    }
    return 0;
}