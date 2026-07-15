const DEADLINE = new Date("2026-06-10T09:10:00+05:30");

function Get_Time_Left() {
    const Now = new Date();
    const Diff = DEADLINE - Now;
    if (Diff <= 0) return { Total_Ms: 0, Days: 0, Hours: 0, Minutes: 0, Seconds: 0, Expired: true };
    const Total_Sec = Math.floor(Diff / 1000);
    return {
        Total_Ms: Diff,
        Days: Math.floor(Total_Sec / 86400),
        Hours: Math.floor((Total_Sec % 86400) / 3600),
        Minutes: Math.floor((Total_Sec % 3600) / 60),
        Seconds: Total_Sec % 60,
        Expired: false
    };
}

function Calc_Avg_Time_Per_Topic() {
    const Left = Count_All_Total() - Count_All_Done();
    const Time = Get_Time_Left();
    if (Time.Expired || Left === 0) return null;
    const Total_Minutes = Math.floor(Time.Total_Ms / 60000);
    const Avg = Math.floor(Total_Minutes / Left);
    const Hrs = Math.floor(Avg / 60);
    const Mins = Avg % 60;
    return { Hrs, Mins, Raw_Mins: Avg };
}

function Pad2(N) {
    return String(N).padStart(2, "0");
}

function Update_Timer_Display() {
    const T = Get_Time_Left();
    const Days_El = document.getElementById("Tmr_Days");
    const Hrs_El = document.getElementById("Tmr_Hrs");
    const Mins_El = document.getElementById("Tmr_Mins");
    const Secs_El = document.getElementById("Tmr_Secs");
    const Avg_El = document.getElementById("Tmr_Avg");
    const Topics_El = document.getElementById("Tmr_Topics_Left");
    const Done_Pct_El = document.getElementById("Tmr_Done_Pct");
    const Deadline_El = document.getElementById("Tmr_Deadline");

    if (T.Expired) {
        if (Days_El) Days_El.textContent = "00";
        if (Hrs_El) Hrs_El.textContent = "00";
        if (Mins_El) Mins_El.textContent = "00";
        if (Secs_El) Secs_El.textContent = "00";
        if (Avg_El) Avg_El.textContent = "—";
        return;
    }

    if (Days_El) Days_El.textContent = Pad2(T.Days);
    if (Hrs_El) Hrs_El.textContent = Pad2(T.Hours);
    if (Mins_El) Mins_El.textContent = Pad2(T.Minutes);
    if (Secs_El) Secs_El.textContent = Pad2(T.Seconds);

    const Avg = Calc_Avg_Time_Per_Topic();
    if (Avg_El) {
        if (!Avg) {
            Avg_El.textContent = "—";
        } else if (Avg.Hrs > 0) {
            Avg_El.textContent = Avg.Hrs + "h " + Avg.Mins + "m";
        } else {
            Avg_El.textContent = Avg.Mins + " min";
        }
    }

    const Left = Count_All_Total() - Count_All_Done();
    if (Topics_El) Topics_El.textContent = Left;

    const Done = Count_All_Done();
    const Total = Count_All_Total();
    const Pct = Total > 0 ? Math.round((Done / Total) * 100) : 0;
    if (Done_Pct_El) Done_Pct_El.textContent = Pct + "%";

    if (Deadline_El) Deadline_El.textContent = "Jun 1, 2026 · 8:30 AM";
}

function Start_Timer() {
    Update_Timer_Display();
    setInterval(Update_Timer_Display, 1000);
}
