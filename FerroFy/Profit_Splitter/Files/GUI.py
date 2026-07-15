import tkinter as Tk
from tkinter import messagebox as Messagebox
from datetime import datetime

from Files.Data_Manager import Data_Manager
from Files.GUI_Modules.Constants import Bg_Main, Bg_Panel, Bg_Card, Border_Glow, Accent_Gold, Accent_Cyan, Txt_Color
from Files.GUI_Modules.Graph_View   import Graph_Overlay
from Files.GUI_Modules.Pie_View     import Pie_Overlay
from Files.GUI_Modules.Summary_View import Summary_Overlay
from Files.GUI_Modules.Goal_View    import Goal_Overlay
from Files.GUI_Modules.History_View import History_Overlay
from Files.GUI_Modules.Header_Bar   import Build_Header
from Files.GUI_Modules.Balance_Panel import Build_Balance_Panel, Update_Balance_Display
from Files.GUI_Modules.Action_Forms  import Setup_Action_Forms, Do_Resell, Do_Rewards, Do_Loan, Do_Transfer, Do_Spend


class Premium_Gui:
    def __init__(self):
        self.Dm = Data_Manager()

        self.Root = Tk.Tk()
        self.Root.title("FerroFy Profit Splitter")
        self.Root.geometry("1440x900")
        try:
            self.Root.state("zoomed")
        except Exception:
            pass
        self.Root.configure(bg=Bg_Main)

        self.Graph_View   = Graph_Overlay(self)
        self.Pie_View     = Pie_Overlay(self)
        self.Summary_View = Summary_Overlay(self)
        self.Goal_View    = Goal_Overlay(self)
        self.History_View = History_Overlay(self)

        self._Build_Header()
        self._Build_Body()
        self.Update_Balance_Display()

        self.Pulse_Step = 0
        self.Animate_Pulse()
        self.Tick_Clock()

        self.Root.protocol("WM_DELETE_WINDOW", self.Confirm_Exit)

    def _Build_Header(self):
        Build_Header(self)

    def _Build_Body(self):
        Body = Tk.Frame(self.Root, bg=Bg_Main)
        Body.pack(fill=Tk.BOTH, expand=True, padx=20, pady=(10, 16))

        Left_Panel = Tk.Frame(Body, bg=Bg_Panel, highlightbackground=Border_Glow, highlightthickness=1)
        Left_Panel.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True, padx=(0, 14))

        Right_Panel = Tk.Frame(Body, bg=Bg_Panel, width=420, highlightbackground=Border_Glow, highlightthickness=1)
        Right_Panel.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        Right_Panel.pack_propagate(False)

        Build_Balance_Panel(self, Right_Panel)
        Setup_Action_Forms(self, Left_Panel)

    def Update_Balance_Display(self):
        Update_Balance_Display(self)

    def Do_Resell(self):
        Do_Resell(self)

    def Do_Rewards(self):
        Do_Rewards(self)

    def Do_Loan(self):
        Do_Loan(self)

    def Do_Transfer(self):
        Do_Transfer(self)

    def Do_Spend(self):
        Do_Spend(self)

    def Clear_Inputs(self, Vars):
        for V in Vars: V.set("")

    def Do_Save(self):
        if self.Dm.Save_Savings():
            Messagebox.showinfo("Saved", "✅  Balances Saved To Money.py!")
        else:
            Messagebox.showerror("Error", "❌  Could Not Save Money.py!")

    def Animate_Pulse(self):
        Cyan_Colors = ["#00BFAA", "#00DDCC", "#00FFEA", "#80FFEF", "#00FFEA", "#00DDCC"]
        C_Idx = (self.Pulse_Step // 4) % len(Cyan_Colors)
        try:
            self.Balance_Text.tag_configure("LabelTag", foreground=Cyan_Colors[C_Idx])
        except Exception:
            pass
        self.Pulse_Step += 1
        self.Root.after(110, self.Animate_Pulse)

    def Tick_Clock(self):
        try:
            Now = datetime.now()
            self.Clock_Label.config(text=Now.strftime("%d %b %Y   %H:%M:%S"))
        except Exception:
            pass
        self.Root.after(1000, self.Tick_Clock)

    def Confirm_Exit(self):
        self.Root.destroy()


def Run_Gui():
    App = Premium_Gui()
    App.Root.mainloop()