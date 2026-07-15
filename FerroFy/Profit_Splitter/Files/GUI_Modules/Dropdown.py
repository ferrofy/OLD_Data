import tkinter as Tk
from Files.GUI_Modules.Constants import (
    Border_Glow, Bg_Input, Txt_Muted, Txt_Color,
    Bg_Card, Accent_Gold_Light, Glow_Gold, Accent_Gold,
)

class Custom_Dropdown:
    Max_Visible = 12

    def __init__(self, Master, Root, Var, Options_Colored):
        self.Root       = Root
        self.Var        = Var
        self.Options    = Options_Colored
        self._Popup     = None
        self._Lb        = None
        self._Bind_Id   = None

        self.Frame = Tk.Frame(Master, bg=Border_Glow, padx=1, pady=1)

        self._Display = Tk.Label(
            self.Frame,
            text="— Select Category —",
            fg=Txt_Muted,
            bg=Bg_Input,
            font=("Segoe UI", 13),
            cursor="hand2",
            anchor="center",
        )
        self._Display.pack(fill=Tk.BOTH, expand=True, ipadx=10, ipady=11)

        self.Var.trace_add("write", self._Sync_Display)
        self.Frame.bind("<Button-1>", self._Toggle)
        self._Display.bind("<Button-1>", self._Toggle)

    def pack(self, **Kw):
        self.Frame.pack(**Kw)

    def _Sync_Display(self, *_):
        Val = self.Var.get().strip()
        if Val:
            Color = Txt_Color
            for Txt, C in self.Options:
                if Txt.strip() == Val:
                    Color = C
                    break
            self._Display.config(text=Val, fg=Color)
        else:
            self._Display.config(text="— Select Category —", fg=Txt_Muted)

    def _Toggle(self, _=None):
        if self._Popup and self._Popup.winfo_exists():
            self._Close()
        else:
            self._Open()

    def _Open(self):
        if self._Popup and self._Popup.winfo_exists():
            self._Close()
            return

        self.Root.update_idletasks()
        X = self.Frame.winfo_rootx()
        Y = self.Frame.winfo_rooty() + self.Frame.winfo_height() + 2
        W = self.Frame.winfo_width()

        self._Popup = Tk.Toplevel(self.Root)
        self._Popup.overrideredirect(True)
        self._Popup.configure(bg=Border_Glow)
        self._Popup.attributes("-topmost", True)

        Visible = min(self.Max_Visible, len(self.Options))
        Lb = Tk.Listbox(
            self._Popup,
            bg=Bg_Card,
            fg=Accent_Gold_Light,
            selectbackground=Glow_Gold,
            selectforeground=Accent_Gold,
            font=("Segoe UI", 12),
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activestyle="none",
            height=Visible,
        )
        Lb.pack(fill=Tk.BOTH, expand=True, padx=1, pady=1)
        self._Lb = Lb

        for I, (Txt, Col) in enumerate(self.Options):
            Lb.insert(Tk.END, f"  {Txt}")
            Lb.itemconfigure(I, foreground=Col)

        self.Root.update_idletasks()
        H = self._Popup.winfo_reqheight()
        self._Popup.geometry(f"{W}x{H}+{X}+{Y}")

        Lb.bind("<<ListboxSelect>>", self._On_Select)
        Lb.bind("<MouseWheel>", lambda E: Lb.yview_scroll(int(-1 * (E.delta / 120)), "units"))
        Lb.bind("<Escape>", lambda _: self._Close())

        self._Bind_Id = self.Root.bind("<ButtonPress-1>", self._On_Root_Press, "+")
        Lb.focus_set()

    def _On_Select(self, _=None):
        if not self._Lb:
            return
        Sel = self._Lb.curselection()
        if Sel:
            self.Var.set(self.Options[Sel[0]][0].strip())
        self._Close()

    def _On_Root_Press(self, E):
        try:
            if self._Popup and self._Popup.winfo_exists():
                Px = self._Popup.winfo_rootx()
                Py = self._Popup.winfo_rooty()
                Pw = self._Popup.winfo_width()
                Ph = self._Popup.winfo_height()
                if not (Px <= E.x_root <= Px + Pw and Py <= E.y_root <= Py + Ph):
                    self._Close()
        except Exception:
            self._Close()

    def _Close(self):
        if self._Bind_Id:
            try:
                self.Root.unbind("<ButtonPress-1>", self._Bind_Id)
            except Exception:
                pass
            self._Bind_Id = None
        if self._Popup and self._Popup.winfo_exists():
            self._Popup.destroy()
        self._Popup = None
        self._Lb = None
