import tkinter as Tk
from Files.GUI_Modules.Constants import *
from Files.GUI_Modules.Utils import Bind_Hover

class Goal_Overlay:
    def __init__(self, App):
        self.App    = App
        self._Goal  = App.Dm.Goals.get("Goal")
        self._Alert = App.Dm.Goals.get("Alert")

    def Show(self):
        self._Goal  = self.App.Dm.Goals.get("Goal")
        self._Alert = self.App.Dm.Goals.get("Alert")

        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.destroy()

        self.Overlay_Frame = Tk.Frame(
            self.App.Root, bg=Bg_Panel,
            highlightbackground=Accent_Gold_Dark, highlightthickness=2,
        )
        self.Overlay_Frame.place(relx=0.16, rely=0.06, relwidth=0.68, relheight=0.88)

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

        Tk.Label(Top_Bar, text="\U0001f3af  Goal & Alert Manager", bg=Bg_Panel, fg=Accent_Gold,
                 font=("Segoe UI", 18, "bold")).pack(side=Tk.LEFT, padx=20)

        Tk.Frame(self.Overlay_Frame, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=18, pady=2)

        Scroll_Canvas = Tk.Canvas(self.Overlay_Frame, bg=Bg_Main, bd=0, highlightthickness=0)
        Scroll_Canvas.pack(fill=Tk.BOTH, expand=True, padx=16, pady=10)

        Inner = Tk.Frame(Scroll_Canvas, bg=Bg_Main)
        Win_Id = Scroll_Canvas.create_window((0, 0), window=Inner, anchor="nw")

        Inner.bind("<Configure>", lambda E: Scroll_Canvas.configure(scrollregion=Scroll_Canvas.bbox("all")))
        Scroll_Canvas.bind("<Configure>", lambda E: Scroll_Canvas.itemconfig(Win_Id, width=E.width))
        Scroll_Canvas.bind("<MouseWheel>", lambda E: Scroll_Canvas.yview_scroll(int(-1 * E.delta / 120), "units"))

        Current_Total = self.App.Dm.Get_Total_Balance()

        self._Build_Hero(Inner, Current_Total)
        self._Build_Goal_Section(Inner, Current_Total)
        self._Build_Alert_Section(Inner, Current_Total)
        self._Build_Saved_Info(Inner)

    def _Build_Hero(self, Parent, Total):
        Hero = Tk.Frame(Parent, bg=Glow_Gold, highlightbackground=Accent_Gold_Dark, highlightthickness=1)
        Hero.pack(fill=Tk.X, padx=20, pady=(8, 10))
        Tk.Frame(Hero, bg=Accent_Gold, height=2).pack(fill=Tk.X)
        Tk.Label(Hero, text="\U0001f4bc  Current Portfolio Total", bg=Glow_Gold, fg=Txt_Muted,
                 font=("Segoe UI", 11), pady=8).pack()
        Clr = Accent_Green if Total >= 0 else Accent_Red
        Tk.Label(Hero, text=f"\u20b9{Total:,.2f}", bg=Glow_Gold, fg=Clr,
                 font=("Segoe UI", 28, "bold"), pady=4).pack()
        Tk.Label(Hero, text="Live Balance \u2014 Updates On Each Action", bg=Glow_Gold, fg=Txt_Muted,
                 font=("Segoe UI", 9), pady=6).pack()

    def _Build_Goal_Section(self, Parent, Current_Total):
        Card = Tk.Frame(Parent, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
        Card.pack(fill=Tk.X, padx=20, pady=8)
        Tk.Frame(Card, bg=Accent_Green, height=3).pack(fill=Tk.X)

        Tk.Label(Card, text="\U0001f3af  Target Balance Goal", bg=Bg_Card, fg=Accent_Green,
                 font=("Segoe UI", 14, "bold"), pady=10, anchor="w").pack(fill=Tk.X, padx=18)

        self.Goal_Var = Tk.StringVar(value="" if self._Goal is None else str(self._Goal))

        Row = Tk.Frame(Card, bg=Bg_Card)
        Row.pack(padx=18, pady=6, fill=Tk.X)

        self._Goal_EF = Tk.Frame(Row, bg="#1A3D1A", padx=1, pady=1)
        self._Goal_EF.pack(side=Tk.LEFT, expand=True, fill=Tk.X)

        Goal_Entry = Tk.Entry(
            self._Goal_EF, textvariable=self.Goal_Var, bg=Bg_Input, fg=Accent_Green,
            font=("Segoe UI", 15), insertbackground=Accent_Green, relief="flat", justify="center",
        )
        Goal_Entry.pack(fill=Tk.X, ipadx=10, ipady=10)
        Goal_Entry.bind("<FocusIn>",  lambda _: self._Goal_EF.config(bg=Accent_Green))
        Goal_Entry.bind("<FocusOut>", lambda _: self._Goal_EF.config(bg="#1A3D1A"))
        Goal_Entry.bind("<Return>",   lambda _: self._Apply_Goal())

        Set_Btn = Tk.Button(Row, text="Set Goal", bg=Accent_Green, fg="#000000",
                            font=("Segoe UI", 12, "bold"), borderwidth=0, cursor="hand2",
                            command=self._Apply_Goal)
        Set_Btn.pack(side=Tk.LEFT, padx=(10, 0), ipadx=14, ipady=10)
        Bind_Hover(Set_Btn, Accent_Green, "#50FF50", "#000000", "#000000")

        self.Goal_Status = Tk.Label(Card, text="", bg=Bg_Card, fg=Txt_Muted,
                                    font=("Segoe UI", 11), pady=6)
        self.Goal_Status.pack(fill=Tk.X, padx=18)

        self.Goal_Bar_Canvas = Tk.Canvas(Card, bg=Bg_Card, height=16, bd=0, highlightthickness=0)
        self.Goal_Bar_Canvas.pack(fill=Tk.X, padx=18, pady=(0, 14))
        self.Goal_Bar_Canvas.bind("<Configure>", lambda E: self._Redraw_Bar_On_Resize())

        if self._Goal is not None:
            self._Refresh_Goal_Status(Current_Total)

    def _Build_Alert_Section(self, Parent, Current_Total):
        Card = Tk.Frame(Parent, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
        Card.pack(fill=Tk.X, padx=20, pady=8)
        Tk.Frame(Card, bg=Accent_Red, height=3).pack(fill=Tk.X)

        Tk.Label(Card, text="\U0001f514  Low Balance Alert Threshold", bg=Bg_Card, fg=Accent_Red,
                 font=("Segoe UI", 14, "bold"), pady=10, anchor="w").pack(fill=Tk.X, padx=18)

        self.Alert_Var = Tk.StringVar(value="" if self._Alert is None else str(self._Alert))

        Row = Tk.Frame(Card, bg=Bg_Card)
        Row.pack(padx=18, pady=6, fill=Tk.X)

        self._Alert_EF = Tk.Frame(Row, bg="#3D1A1A", padx=1, pady=1)
        self._Alert_EF.pack(side=Tk.LEFT, expand=True, fill=Tk.X)

        Alert_Entry = Tk.Entry(
            self._Alert_EF, textvariable=self.Alert_Var, bg=Bg_Input, fg=Accent_Red,
            font=("Segoe UI", 15), insertbackground=Accent_Red, relief="flat", justify="center",
        )
        Alert_Entry.pack(fill=Tk.X, ipadx=10, ipady=10)
        Alert_Entry.bind("<FocusIn>",  lambda _: self._Alert_EF.config(bg=Accent_Red))
        Alert_Entry.bind("<FocusOut>", lambda _: self._Alert_EF.config(bg="#3D1A1A"))
        Alert_Entry.bind("<Return>",   lambda _: self._Apply_Alert())

        Set_Btn = Tk.Button(Row, text="Set Alert", bg=Accent_Red, fg="#FFFFFF",
                            font=("Segoe UI", 12, "bold"), borderwidth=0, cursor="hand2",
                            command=self._Apply_Alert)
        Set_Btn.pack(side=Tk.LEFT, padx=(10, 0), ipadx=14, ipady=10)
        Bind_Hover(Set_Btn, Accent_Red, "#FF6666", "#FFFFFF", "#FFFFFF")

        self.Alert_Status = Tk.Label(Card, text="", bg=Bg_Card, fg=Txt_Muted,
                                     font=("Segoe UI", 11), pady=6)
        self.Alert_Status.pack(fill=Tk.X, padx=18)

        if self._Alert is not None:
            self._Refresh_Alert_Status(Current_Total)

    def _Build_Saved_Info(self, Parent):
        Card = Tk.Frame(Parent, bg=Bg_Card, highlightbackground=Border_Glow, highlightthickness=1)
        Card.pack(fill=Tk.X, padx=20, pady=(4, 16))
        Tk.Frame(Card, bg=Accent_Cyan_Dark, height=3).pack(fill=Tk.X)

        Tk.Label(Card, text="\U0001f4be  Persisted Settings", bg=Bg_Card, fg=Accent_Cyan,
                 font=("Segoe UI", 13, "bold"), pady=8, anchor="w").pack(fill=Tk.X, padx=18)

        Goal_Txt  = f"\u20b9{self._Goal:,.2f}"  if self._Goal  is not None else "Not Set"
        Alert_Txt = f"\u20b9{self._Alert:,.2f}" if self._Alert is not None else "Not Set"

        for Lbl, Val in [("Saved Goal", Goal_Txt), ("Saved Alert", Alert_Txt)]:
            Row = Tk.Frame(Card, bg=Bg_Card)
            Row.pack(fill=Tk.X, padx=18, pady=4)
            Tk.Label(Row, text=Lbl, bg=Bg_Card, fg=Txt_Muted, font=("Segoe UI", 11), anchor="w").pack(side=Tk.LEFT)
            Tk.Label(Row, text=Val, bg=Bg_Card, fg=Accent_Cyan_Dark if Val == "Not Set" else Accent_Gold_Light,
                     font=("Segoe UI", 11, "bold"), anchor="e").pack(side=Tk.RIGHT)

        Tk.Label(Card, text="Auto-saved to Goals.json \u2014 Restored On Next Launch",
                 bg=Bg_Card, fg=Txt_Muted, font=("Segoe UI", 9), pady=8).pack()

    def _Redraw_Bar_On_Resize(self):
        if self._Goal is not None:
            Pct = min((self.App.Dm.Get_Total_Balance() / self._Goal) * 100, 100) if self._Goal > 0 else 0
            self._Draw_Progress_Bar(Pct)

    def _Draw_Progress_Bar(self, Pct):
        try:
            C = self.Goal_Bar_Canvas
            C.delete("all")
            C.update_idletasks()
            W = C.winfo_width()
            if W < 10:
                return
            C.create_rectangle(0, 2, W, 14, fill=Border_Glow, outline="")
            Fill_W = max(12, int(W * min(Pct, 100) / 100))
            Clr    = Accent_Gold if Pct >= 100 else Accent_Green
            C.create_rectangle(0, 2, Fill_W, 14, fill=Clr, outline="")
            Pct_Lbl = f"  {min(Pct, 100):.1f}%"
            C.create_text(W // 2, 8, text=Pct_Lbl, fill="#000000" if Fill_W > W // 2 else Txt_Muted, font=("Segoe UI", 8, "bold"))
        except Exception:
            pass

    def _Apply_Goal(self):
        try:
            Val = float(self.Goal_Var.get().strip())
            self._Goal = Val
            self.App.Dm.Goals["Goal"] = Val
            self.App.Dm.Save_Goals()
            self._Refresh_Goal_Status(self.App.Dm.Get_Total_Balance())
        except Exception:
            self.Goal_Status.config(text="\u26a0  Enter A Valid Number", fg=Accent_Red)

    def _Refresh_Goal_Status(self, Current):
        if self._Goal is None:
            return
        Remaining = self._Goal - Current
        Pct       = min((Current / self._Goal) * 100, 100) if self._Goal > 0 else 0
        if Remaining <= 0:
            self.Goal_Status.config(
                text=f"\u2705  Goal \u20b9{self._Goal:,.2f} Reached!  +\u20b9{abs(Remaining):,.2f} Extra",
                fg=Accent_Green,
            )
        else:
            self.Goal_Status.config(
                text=f"\u20b9{Remaining:,.2f} Remaining  |  {Pct:.1f}% Complete",
                fg=Accent_Gold_Light,
            )
        self.Goal_Bar_Canvas.update_idletasks()
        self._Draw_Progress_Bar(Pct)

    def _Apply_Alert(self):
        try:
            Val = float(self.Alert_Var.get().strip())
            self._Alert = Val
            self.App.Dm.Goals["Alert"] = Val
            self.App.Dm.Save_Goals()
            self._Refresh_Alert_Status(self.App.Dm.Get_Total_Balance())
        except Exception:
            self.Alert_Status.config(text="\u26a0  Enter A Valid Number", fg=Accent_Red)

    def _Refresh_Alert_Status(self, Current):
        if self._Alert is None:
            return
        if Current <= self._Alert:
            self.Alert_Status.config(
                text=f"\U0001f534  ALERT! \u20b9{Current:,.2f} Is Below Threshold \u20b9{self._Alert:,.2f}",
                fg=Accent_Red,
            )
        else:
            Margin = Current - self._Alert
            self.Alert_Status.config(
                text=f"\U0001f7e2  Safe  |  \u20b9{Margin:,.2f} Above Alert Level",
                fg=Accent_Green,
            )

    def Hide(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.place_forget()
            self.Overlay_Frame.destroy()
