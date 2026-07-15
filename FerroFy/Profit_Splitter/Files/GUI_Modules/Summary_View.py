import tkinter as Tk
import statistics
from Files.GUI_Modules.Constants import *
from Files.GUI_Modules.Utils import Bind_Hover

class Summary_Overlay:
    def __init__(self, App):
        self.App        = App
        self._Anim_Step = 0
        self._Anim_Id   = None

    def Show(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.destroy()
        if self._Anim_Id:
            try:
                self.App.Root.after_cancel(self._Anim_Id)
            except Exception:
                pass
            self._Anim_Id = None

        self.Overlay_Frame = Tk.Frame(
            self.App.Root, bg=Bg_Panel,
            highlightbackground=Accent_Gold_Dark, highlightthickness=2,
        )
        self.Overlay_Frame.place(relx=0.04, rely=0.04, relwidth=0.92, relheight=0.92)

        Tk.Frame(self.Overlay_Frame, bg=Accent_Gold_Dark, height=3).pack(fill=Tk.X)

        Top_Bar = Tk.Frame(self.Overlay_Frame, bg=Bg_Panel)
        Top_Bar.pack(fill=Tk.X, pady=10, padx=18)

        Back_Btn = Tk.Button(
            Top_Bar, text="\u2b05  Back", bg=Bg_Card, fg=Accent_Gold_Light,
            font=("Segoe UI", 12, "bold"), borderwidth=0, cursor="hand2",
            command=self.Hide, activebackground=Accent_Gold_Dark,
        )
        Back_Btn.pack(side=Tk.LEFT, ipadx=16, ipady=7)
        Bind_Hover(Back_Btn, Bg_Card, Border_Glow, Accent_Gold_Light, Accent_Gold)

        Tk.Label(Top_Bar, text="\U0001f4ca  Summary Statistics", bg=Bg_Panel, fg=Accent_Gold,
                 font=("Segoe UI", 18, "bold")).pack(side=Tk.LEFT, padx=20)

        Tk.Frame(self.Overlay_Frame, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=18, pady=2)

        Scroll_Canvas = Tk.Canvas(self.Overlay_Frame, bg=Bg_Main, bd=0, highlightthickness=0)
        Scroll_Canvas.pack(fill=Tk.BOTH, expand=True, padx=14, pady=10)

        Inner = Tk.Frame(Scroll_Canvas, bg=Bg_Main)
        Win_Id = Scroll_Canvas.create_window((0, 0), window=Inner, anchor="nw")

        Inner.bind("<Configure>", lambda E: Scroll_Canvas.configure(scrollregion=Scroll_Canvas.bbox("all")))
        Scroll_Canvas.bind("<Configure>", lambda E: Scroll_Canvas.itemconfig(Win_Id, width=E.width))
        Scroll_Canvas.bind("<MouseWheel>", lambda E: Scroll_Canvas.yview_scroll(int(-1 * E.delta / 120), "units"))
        Inner.bind("<MouseWheel>", lambda E: Scroll_Canvas.yview_scroll(int(-1 * E.delta / 120), "units"))

        self.Build_Stats(Inner)

    def _Compute(self):
        Dm           = self.App.Dm
        History      = Dm.History
        Savings      = Dm.Savings

        Balances     = {Item[0].strip(): float(Item[1]) for Item in Savings if isinstance(Item, list)}
        Hist_Keys    = list(History.keys())
        Hist_Vals    = Dm.Get_Hist_Balances()

        Total        = sum(Balances.values())
        Max_Bal      = max(Hist_Vals) if Hist_Vals else Total
        Min_Bal      = min(Hist_Vals) if Hist_Vals else Total
        Avg_Bal      = statistics.mean(Hist_Vals) if Hist_Vals else Total
        Std_Dev      = statistics.stdev(Hist_Vals) if len(Hist_Vals) > 1 else 0.0

        Best_Cat     = max(Balances, key=Balances.get) if Balances else "—"
        Worst_Cat    = min(Balances, key=Balances.get) if Balances else "—"
        Best_Val     = Balances.get(Best_Cat, 0.0)
        Worst_Val    = Balances.get(Worst_Cat, 0.0)

        Pos_Count    = sum(1 for V in Balances.values() if V > 0)
        Neg_Count    = sum(1 for V in Balances.values() if V < 0)
        Zero_Count   = sum(1 for V in Balances.values() if V == 0)

        Daily_Change  = 0.0
        Daily_Pct     = 0.0
        if len(Hist_Vals) >= 2:
            Daily_Change = Hist_Vals[-1] - Hist_Vals[-2]
            if Hist_Vals[-2] != 0:
                Daily_Pct = (Daily_Change / abs(Hist_Vals[-2])) * 100

        Weekly_Change = 0.0
        if len(Hist_Vals) >= 7:
            Weekly_Change = Hist_Vals[-1] - Hist_Vals[-7]
        elif len(Hist_Vals) >= 2:
            Weekly_Change = Hist_Vals[-1] - Hist_Vals[0]

        Monthly_Change = 0.0
        if len(Hist_Vals) >= 30:
            Monthly_Change = Hist_Vals[-1] - Hist_Vals[-30]
        elif len(Hist_Vals) >= 2:
            Monthly_Change = Hist_Vals[-1] - Hist_Vals[0]

        Best_Day_Gain = 0.0
        Best_Day_Loss = 0.0
        if len(Hist_Vals) >= 2:
            Daily_Deltas  = [Hist_Vals[I] - Hist_Vals[I - 1] for I in range(1, len(Hist_Vals))]
            Best_Day_Gain = max(Daily_Deltas)
            Best_Day_Loss = min(Daily_Deltas)

        Rise_Streak  = 0
        for I in range(len(Hist_Vals) - 1, 0, -1):
            if Hist_Vals[I] > Hist_Vals[I - 1]: Rise_Streak += 1
            else: break

        Fall_Streak  = 0
        for I in range(len(Hist_Vals) - 1, 0, -1):
            if Hist_Vals[I] < Hist_Vals[I - 1]: Fall_Streak += 1
            else: break

        Above_Avg    = sum(1 for V in Hist_Vals if V > Avg_Bal)
        Below_Avg    = sum(1 for V in Hist_Vals if V < Avg_Bal)
        Median_Bal   = statistics.median(Hist_Vals) if Hist_Vals else Total

        Total_Invested = sum(V for V in Balances.values() if V > 0)
        Total_Deficit  = sum(V for V in Balances.values() if V < 0)
        Portfolio_Util = (Total / Total_Invested * 100) if Total_Invested > 0 else 0.0

        Growth = 0.0
        if len(Hist_Vals) >= 2 and Hist_Vals[0] != 0:
            Growth = ((Hist_Vals[-1] - Hist_Vals[0]) / abs(Hist_Vals[0])) * 100

        return {
            "Balances": Balances, "Hist_Keys": Hist_Keys, "Hist_Vals": Hist_Vals,
            "Total": Total, "Max_Bal": Max_Bal, "Min_Bal": Min_Bal, "Avg_Bal": Avg_Bal,
            "Std_Dev": Std_Dev, "Best_Cat": Best_Cat, "Worst_Cat": Worst_Cat,
            "Best_Val": Best_Val, "Worst_Val": Worst_Val,
            "Pos_Count": Pos_Count, "Neg_Count": Neg_Count, "Zero_Count": Zero_Count,
            "Daily_Change": Daily_Change, "Daily_Pct": Daily_Pct,
            "Weekly_Change": Weekly_Change, "Monthly_Change": Monthly_Change,
            "Best_Day_Gain": Best_Day_Gain, "Best_Day_Loss": Best_Day_Loss,
            "Rise_Streak": Rise_Streak, "Fall_Streak": Fall_Streak,
            "Above_Avg": Above_Avg, "Below_Avg": Below_Avg,
            "Median_Bal": Median_Bal, "Total_Invested": Total_Invested,
            "Total_Deficit": Total_Deficit, "Portfolio_Util": Portfolio_Util,
            "Growth": Growth,
        }

    def _Card(self, Parent, Title, Strip_Color):
        Card = Tk.Frame(Parent, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
        Card.pack(fill=Tk.X, padx=20, pady=7)
        Tk.Frame(Card, bg=Strip_Color, height=3).pack(fill=Tk.X)
        Tk.Label(Card, text=Title, bg=Bg_Card, fg=Strip_Color, font=("Segoe UI", 13, "bold"),
                 pady=8, anchor="w").pack(fill=Tk.X, padx=16)
        Tk.Frame(Card, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=12, pady=2)
        return Card

    def _Row(self, Card, Label, Value, Clr):
        Row = Tk.Frame(Card, bg=Bg_Card)
        Row.pack(fill=Tk.X, padx=16, pady=4)
        Tk.Label(Row, text=Label, bg=Bg_Card, fg=Txt_Muted, font=("Segoe UI", 11), anchor="w").pack(side=Tk.LEFT)
        Lbl = Tk.Label(Row, text=Value, bg=Bg_Card, fg=Clr, font=("Segoe UI", 11, "bold"), anchor="e")
        Lbl.pack(side=Tk.RIGHT)
        return Lbl

    def Build_Stats(self, Parent):
        D = self._Compute()

        Tk.Frame(Parent, bg=Bg_Main, height=6).pack(fill=Tk.X)

        Hero_Row = Tk.Frame(Parent, bg=Bg_Main)
        Hero_Row.pack(fill=Tk.X, padx=14, pady=(0, 6))

        Daily_Clr  = Accent_Green if D["Daily_Change"] >= 0 else Accent_Red
        Pct_Clr    = Accent_Green if D["Daily_Pct"]    >= 0 else Accent_Red
        Pct_Sign   = "+" if D["Daily_Pct"]    >= 0 else ""
        Change_Sign = "+" if D["Daily_Change"] >= 0 else ""

        for Title, Val, Sub, Clr, Strip in [
            ("Total Balance",    f"\u20b9{D['Total']:,.2f}",                     f"{len(D['Balances'])} Categories", Accent_Gold,  Accent_Gold),
            ("Today's Change",   f"{Change_Sign}\u20b9{D['Daily_Change']:,.2f}", "Vs Yesterday (\u20b9)",            Daily_Clr,    Daily_Clr),
            ("Today's Change %", f"{Pct_Sign}{D['Daily_Pct']:.2f}%",            "Vs Yesterday (%)",                 Pct_Clr,      Pct_Clr),
        ]:
            F = Tk.Frame(Hero_Row, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
            F.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True, padx=5, pady=5)
            Tk.Frame(F, bg=Strip, height=2).pack(fill=Tk.X)
            Tk.Label(F, text=Title, bg=Bg_Card, fg=Txt_Muted,  font=("Segoe UI", 9),           pady=6).pack()
            Tk.Label(F, text=Val,   bg=Bg_Card, fg=Clr,        font=("Segoe UI", 15, "bold"),  pady=2).pack()
            Tk.Label(F, text=Sub,   bg=Bg_Card, fg=Txt_Muted,  font=("Segoe UI", 8),           pady=5).pack()

        C1 = self._Card(Parent, "\U0001f4b0  Balance Overview", Accent_Gold)
        for Lbl, Val, Clr in [
            ("All-Time High",    f"\u20b9{D['Max_Bal']:,.2f}",      Accent_Green),
            ("All-Time Low",     f"\u20b9{D['Min_Bal']:,.2f}",      Accent_Red),
            ("Average Balance",  f"\u20b9{D['Avg_Bal']:,.2f}",      Accent_Gold_Light),
            ("Median Balance",   f"\u20b9{D['Median_Bal']:,.2f}",   Accent_Cyan),
            ("Volatility (Std)", f"\u20b9{D['Std_Dev']:,.2f}",      Txt_Muted),
        ]:
            self._Row(C1, Lbl, Val, Clr)

        C2 = self._Card(Parent, "\U0001f4c8  Profit & Loss", Accent_Cyan)
        Dc  = D["Daily_Change"]
        Wc  = D["Weekly_Change"]
        Mc  = D["Monthly_Change"]
        for Lbl, Val, Clr in [
            ("Today's Change",   f"{'+'  if Dc >= 0 else ''}\u20b9{Dc:,.2f}",        Accent_Green if Dc >= 0 else Accent_Red),
            ("Today's Change %", f"{Pct_Sign}{D['Daily_Pct']:.2f}%",                  Accent_Green if D["Daily_Pct"] >= 0 else Accent_Red),
            ("Weekly Change",    f"{'+'  if Wc >= 0 else ''}\u20b9{Wc:,.2f}",        Accent_Green if Wc >= 0 else Accent_Red),
            ("Monthly Change",   f"{'+'  if Mc >= 0 else ''}\u20b9{Mc:,.2f}",        Accent_Green if Mc >= 0 else Accent_Red),
            ("Best Single Day",  f"+\u20b9{D['Best_Day_Gain']:,.2f}",                 Accent_Green),
            ("Worst Single Day", f"\u20b9{D['Best_Day_Loss']:,.2f}",                  Accent_Red),
        ]:
            self._Row(C2, Lbl, Val, Clr)

        C3 = self._Card(Parent, "\U0001f4c2  Category Breakdown", Accent_Purple)
        for Lbl, Val, Clr in [
            ("Total Categories",   str(len(D["Balances"])),              Accent_Cyan),
            ("In Profit",          f"{D['Pos_Count']} Categories",       Accent_Green),
            ("In Deficit",         f"{D['Neg_Count']} Categories",       Accent_Red),
            ("At Zero",            f"{D['Zero_Count']} Categories",      Txt_Muted),
            ("Total Positive Sum", f"\u20b9{D['Total_Invested']:,.2f}",  Accent_Green),
            ("Total Deficit Sum",  f"\u20b9{D['Total_Deficit']:,.2f}",   Accent_Red),
            ("Portfolio Util.",    f"{D['Portfolio_Util']:.1f}%",        Accent_Gold),
        ]:
            self._Row(C3, Lbl, Val, Clr)

        C4 = self._Card(Parent, "\U0001f3c6  Leaders & Streaks", Accent_Gold)
        for Lbl, Val, Clr in [
            ("Best Category",  f"{D['Best_Cat']}  (\u20b9{D['Best_Val']:,.2f})",   Accent_Gold),
            ("Worst Category", f"{D['Worst_Cat']}  (\u20b9{D['Worst_Val']:,.2f})", Accent_Red),
            ("Rising Streak",  f"{D['Rise_Streak']} Day(s) In A Row",               Accent_Green),
            ("Falling Streak", f"{D['Fall_Streak']} Day(s) In A Row",               Accent_Red),
            ("Days Above Avg", f"{D['Above_Avg']} Days",                             Accent_Cyan),
            ("Days Below Avg", f"{D['Below_Avg']} Days",                             Txt_Muted),
            ("Overall Growth", f"{D['Growth']:+.2f}%",                               Accent_Green if D["Growth"] >= 0 else Accent_Red),
        ]:
            self._Row(C4, Lbl, Val, Clr)

        C5 = self._Card(Parent, "\U0001f5c2  History Snapshot", Accent_Purple)
        Hk = D["Hist_Keys"]
        Hv = D["Hist_Vals"]
        for Lbl, Val, Clr in [
            ("Recorded Days",  str(len(Hk)),                                 Accent_Purple),
            ("First Record",   Hk[0]  if Hk else "\u2014",                  Txt_Muted),
            ("Latest Record",  Hk[-1] if Hk else "\u2014",                  Txt_Muted),
            ("First Balance",  f"\u20b9{Hv[0]:,.2f}"  if Hv else "\u2014",  Txt_Muted),
            ("Latest Balance", f"\u20b9{Hv[-1]:,.2f}" if Hv else "\u2014",  Accent_Gold_Light),
        ]:
            self._Row(C5, Lbl, Val, Clr)

        Tk.Frame(Parent, bg=Bg_Main, height=12).pack(fill=Tk.X)

        self._Animate_Cards(Parent)

    def _Animate_Cards(self, Parent):
        Cards = [W for W in Parent.winfo_children() if isinstance(W, Tk.Frame)]
        self._Fade_In_Cards(Cards, 0)

    def _Fade_In_Cards(self, Cards, Index):
        if Index >= len(Cards):
            return
        try:
            Cards[Index].config(highlightcolor=Accent_Gold)
        except Exception:
            pass
        self._Anim_Id = self.App.Root.after(60, lambda: self._Fade_In_Cards(Cards, Index + 1))

    def Hide(self):
        if self._Anim_Id:
            try:
                self.App.Root.after_cancel(self._Anim_Id)
            except Exception:
                pass
            self._Anim_Id = None
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.place_forget()
            self.Overlay_Frame.destroy()
