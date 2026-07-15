import tkinter as Tk
from tkinter import ttk as Ttk
from tkinter import messagebox as Messagebox

from Files import Actions as Actions
from Files.GUI_Modules.Constants import (
    Bg_Panel, Bg_Card, Bg_Input, Border_Glow,
    Accent_Gold, Accent_Gold_Dark, Accent_Cyan, Accent_Cyan_Dark,
    Glow_Gold, Txt_Muted, Font_Tab, Font_Main,
)
from Files.GUI_Modules.Utils import Bind_Hover, Create_Scrollable_Tab, Parse_Float, Parse_Int
from Files.GUI_Modules.Dropdown import Custom_Dropdown

Group_Colors = [
    "#FF6B6B", "#4ECDC4", "#FFD93D", "#6BCB77",
    "#FF8B94", "#C7B8EA", "#74C0FC", "#FFD700",
    "#FFA07A", "#B0E0E6", "#DDA0DD", "#98FB98",
]

def Get_Category_Options_Colored(Gui_Ref):
    Options = []
    Count = 0
    Group_Idx = -1
    for Item in Gui_Ref.Dm.Savings:
        if isinstance(Item, str):
            Group_Idx += 1
        elif isinstance(Item, list):
            Count += 1
            Color = Group_Colors[Group_Idx % len(Group_Colors)]
            Options.append((f"{Count}. {Item[0].strip()}", Color))
    return Options

def Parse_Combo_Index(Combo_Value):
    try:
        Val = Combo_Value.strip()
        if not Val or Val.startswith("—"):
            raise Exception("No Category Selected")
        return int(Val.split(".")[0]) - 1
    except Exception as E:
        raise Exception(str(E))

def Get_Real_Index(Gui_Ref, Visual_Index):
    Count = 0
    for I, Item in enumerate(Gui_Ref.Dm.Savings):
        if isinstance(Item, list):
            if Count == Visual_Index:
                return I
            Count += 1
    return -1

def Setup_Action_Forms(Gui_Ref, Parent):
    Style = Ttk.Style()
    Style.theme_use("default")
    Style.configure("TNotebook",        background=Bg_Panel, borderwidth=0, tabmargins=[0, 0, 0, 0])
    Style.configure("TNotebook.Tab",    background="#08080F",  foreground=Txt_Muted, font=Font_Tab, padding=[24, 11], borderwidth=0)
    Style.map("TNotebook.Tab",
        background=[("selected", Bg_Card)],
        foreground=[("selected", Accent_Cyan)],
        expand=[("selected", [1, 1, 1, 0])],
    )

    Gui_Ref.Notebook = Ttk.Notebook(Parent)
    Gui_Ref.Notebook.pack(fill=Tk.BOTH, expand=True, padx=14, pady=14)

    Gui_Ref.Tab_Resell   = Create_Scrollable_Tab(Gui_Ref.Notebook, "  🔁 Resell  ")
    Gui_Ref.Tab_Rewards  = Create_Scrollable_Tab(Gui_Ref.Notebook, "  🎁 Rewards  ")
    Gui_Ref.Tab_Loan     = Create_Scrollable_Tab(Gui_Ref.Notebook, "  🏦 Loan  ")
    Gui_Ref.Tab_Transfer = Create_Scrollable_Tab(Gui_Ref.Notebook, "  🔀 Transfer  ")
    Gui_Ref.Tab_Spend    = Create_Scrollable_Tab(Gui_Ref.Notebook, "  💸 Spend  ")

    Cat_Opts = Get_Category_Options_Colored(Gui_Ref)

    Gui_Ref.Resell_Cat_Var = Tk.StringVar()
    _Create_Dropdown(Gui_Ref, Gui_Ref.Tab_Resell, "Category:", Gui_Ref.Resell_Cat_Var, Cat_Opts)
    Gui_Ref.Bp_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Resell, "Buying Price (Bp):", "Bp_Var")
    Gui_Ref.Sp_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Resell, "Selling Price (Sp):", "Sp_Var")
    Gui_Ref.Q_Entry  = _Create_Input(Gui_Ref, Gui_Ref.Tab_Resell, "Quantity (Q):", "Q_Var")
    _Add_Run_Btn(Gui_Ref, Gui_Ref.Tab_Resell, Gui_Ref.Do_Resell, [Gui_Ref.Bp_Entry, Gui_Ref.Sp_Entry, Gui_Ref.Q_Entry])

    Gui_Ref.Reward_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Rewards, "Reward Amount:", "Reward_Var")
    _Add_Run_Btn(Gui_Ref, Gui_Ref.Tab_Rewards, Gui_Ref.Do_Rewards, [Gui_Ref.Reward_Entry])

    Gui_Ref.Loan_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Loan, "Loan Amount:", "Loan_Var")
    _Add_Run_Btn(Gui_Ref, Gui_Ref.Tab_Loan, Gui_Ref.Do_Loan, [Gui_Ref.Loan_Entry])

    Gui_Ref.Transfer_From_Var = Tk.StringVar()
    Gui_Ref.Transfer_To_Var   = Tk.StringVar()
    _Create_Dropdown(Gui_Ref, Gui_Ref.Tab_Transfer, "From Category:", Gui_Ref.Transfer_From_Var, Cat_Opts)
    _Create_Dropdown(Gui_Ref, Gui_Ref.Tab_Transfer, "To Category:",   Gui_Ref.Transfer_To_Var,   Cat_Opts)
    Gui_Ref.Transfer_Amt_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Transfer, "Amount:", "Transfer_Amount_Var")
    _Add_Run_Btn(Gui_Ref, Gui_Ref.Tab_Transfer, Gui_Ref.Do_Transfer, [Gui_Ref.Transfer_Amt_Entry])

    Gui_Ref.Spend_Cat_Var = Tk.StringVar()
    _Create_Dropdown(Gui_Ref, Gui_Ref.Tab_Spend, "Category:", Gui_Ref.Spend_Cat_Var, Cat_Opts)
    Gui_Ref.Spend_Amt_Entry = _Create_Input(Gui_Ref, Gui_Ref.Tab_Spend, "Amount:", "Spend_Amount_Var")
    _Add_Run_Btn(Gui_Ref, Gui_Ref.Tab_Spend, Gui_Ref.Do_Spend, [Gui_Ref.Spend_Amt_Entry])

    Gui_Ref.Root.bind_all("<MouseWheel>", lambda E: _On_Mousewheel(Gui_Ref, E))

def _On_Mousewheel(Gui_Ref, E):
    if isinstance(E.widget, Tk.Listbox):
        return
    try:
        Active_Tab_Id = Gui_Ref.Notebook.select()
        if Active_Tab_Id:
            Active_Tab = Gui_Ref.Notebook.nametowidget(Active_Tab_Id)
            for Child in Active_Tab.winfo_children():
                if isinstance(Child, Tk.Canvas):
                    Bbox = Child.bbox("all")
                    if Bbox and Bbox[3] > Child.winfo_height():
                        Child.yview_scroll(int(-1 * (E.delta / 120)), "units")
                    break
    except Exception:
        pass

def _Create_Dropdown(Gui_Ref, Parent, Label_Text, Var, Options_Colored):
    Frame = Tk.Frame(Parent, bg=Bg_Panel)
    Frame.pack(pady=14, fill=Tk.X, padx=50)

    Tk.Label(Frame, text=Label_Text, bg=Bg_Panel, fg=Txt_Muted, font=Font_Main).pack(side=Tk.LEFT)

    Drop_Container = Tk.Frame(Frame, bg=Bg_Panel)
    Drop_Container.pack(side=Tk.RIGHT, expand=True, fill=Tk.X, padx=(24, 0))

    Dd = Custom_Dropdown(Drop_Container, Gui_Ref.Root, Var, Options_Colored)
    Dd.pack(fill=Tk.BOTH, expand=True)
    return Dd

def _Add_Run_Btn(Gui_Ref, Parent, Cmd_Func, Entries):
    Btn_Container = Tk.Frame(Parent, bg=Bg_Panel)
    Btn_Container.pack(fill=Tk.X, pady=(20, 36))

    Outer = Tk.Frame(Btn_Container, bg=Accent_Gold_Dark, padx=2, pady=2)
    Outer.pack()

    Btn = Tk.Button(
        Outer,
        text="⚡  Execute",
        bg=Glow_Gold,
        fg=Accent_Gold,
        font=("Segoe UI", 15, "bold"),
        borderwidth=0,
        cursor="hand2",
        command=Cmd_Func,
        activebackground=Accent_Gold,
        activeforeground="#000000",
    )
    Btn.pack(ipadx=50, ipady=14)
    Bind_Hover(Btn, Glow_Gold, Accent_Gold, Accent_Gold, "#000000")

    for Entry in Entries:
        Entry.bind("<Return>", lambda E, F=Cmd_Func: F())

def _Create_Input(Gui_Ref, Parent, Label_Text, Var_Name):
    Frame = Tk.Frame(Parent, bg=Bg_Panel)
    Frame.pack(pady=14, fill=Tk.X, padx=50)

    Tk.Label(Frame, text=Label_Text, bg=Bg_Panel, fg=Txt_Muted, font=Font_Main).pack(side=Tk.LEFT)
    Var = Tk.StringVar(value="")
    setattr(Gui_Ref, Var_Name, Var)

    Entry_Frame = Tk.Frame(Frame, bg=Accent_Cyan_Dark, padx=1, pady=1)
    Entry_Frame.pack(side=Tk.RIGHT, expand=True, fill=Tk.X, padx=(24, 0))

    Entry = Tk.Entry(
        Entry_Frame,
        textvariable=Var,
        bg=Bg_Input,
        fg=Accent_Cyan,
        font=("Segoe UI", 16),
        insertbackground=Accent_Cyan,
        relief="flat",
        justify="center",
    )
    Entry.pack(fill=Tk.BOTH, expand=True, ipadx=10, ipady=11)

    def On_Focus_In(_):
        Entry_Frame.config(bg=Accent_Cyan)

    def On_Focus_Out(_):
        Entry_Frame.config(bg=Accent_Cyan_Dark)

    Entry.bind("<FocusIn>",  On_Focus_In)
    Entry.bind("<FocusOut>", On_Focus_Out)
    return Entry

def Do_Resell(Gui_Ref):
    try:
        Visual_Idx = Parse_Combo_Index(Gui_Ref.Resell_Cat_Var.get())
        Real_Idx   = Get_Real_Index(Gui_Ref, Visual_Idx)
        if Real_Idx == -1: raise Exception("Invalid Category")
        Bp = Parse_Float(Gui_Ref.Bp_Var.get())
        Sp = Parse_Float(Gui_Ref.Sp_Var.get())
        Q  = Parse_Int(Gui_Ref.Q_Var.get())
        Actions.Resell_Action(Gui_Ref.Dm, Real_Idx, Bp, Sp, Q)
        Gui_Ref.Update_Balance_Display()
        Gui_Ref.Resell_Cat_Var.set("")
        Gui_Ref.Clear_Inputs([Gui_Ref.Bp_Var, Gui_Ref.Sp_Var, Gui_Ref.Q_Var])
    except Exception as E:
        Messagebox.showerror("Error", f"Invalid Input: {E}")

def Do_Rewards(Gui_Ref):
    try:
        Amt = Parse_Float(Gui_Ref.Reward_Var.get())
        Actions.Rewards_Action(Gui_Ref.Dm, Amt)
        Gui_Ref.Update_Balance_Display()
        Gui_Ref.Clear_Inputs([Gui_Ref.Reward_Var])
    except Exception as E:
        Messagebox.showerror("Error", f"Invalid Input: {E}")

def Do_Loan(Gui_Ref):
    try:
        Amt = Parse_Float(Gui_Ref.Loan_Var.get())
        Actions.Loan_Action(Gui_Ref.Dm, Amt)
        Gui_Ref.Update_Balance_Display()
        Gui_Ref.Clear_Inputs([Gui_Ref.Loan_Var])
    except Exception as E:
        Messagebox.showerror("Error", f"Invalid Input: {E}")

def Do_Transfer(Gui_Ref):
    try:
        From_Idx  = Parse_Combo_Index(Gui_Ref.Transfer_From_Var.get())
        To_Idx    = Parse_Combo_Index(Gui_Ref.Transfer_To_Var.get())
        Real_From = Get_Real_Index(Gui_Ref, From_Idx)
        Real_To   = Get_Real_Index(Gui_Ref, To_Idx)
        if Real_From == -1 or Real_To == -1: raise Exception("Invalid Category")
        Amt = Parse_Float(Gui_Ref.Transfer_Amount_Var.get())
        Actions.Transfer_Action(Gui_Ref.Dm, Real_From, Real_To, Amt)
        Gui_Ref.Update_Balance_Display()
        Gui_Ref.Transfer_From_Var.set("")
        Gui_Ref.Transfer_To_Var.set("")
        Gui_Ref.Clear_Inputs([Gui_Ref.Transfer_Amount_Var])
    except Exception as E:
        Messagebox.showerror("Error", f"Invalid Input: {E}")

def Do_Spend(Gui_Ref):
    try:
        Visual_Idx = Parse_Combo_Index(Gui_Ref.Spend_Cat_Var.get())
        Real_Idx   = Get_Real_Index(Gui_Ref, Visual_Idx)
        if Real_Idx == -1: raise Exception("Invalid Category")
        Amt = Parse_Float(Gui_Ref.Spend_Amount_Var.get())
        Actions.Spend_Action(Gui_Ref.Dm, Real_Idx, Amt)
        Gui_Ref.Update_Balance_Display()
        Gui_Ref.Spend_Cat_Var.set("")
        Gui_Ref.Clear_Inputs([Gui_Ref.Spend_Amount_Var])
    except Exception as E:
        Messagebox.showerror("Error", f"Invalid Input: {E}")
