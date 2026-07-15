import tkinter as Tk
from tkinter import ttk as Ttk
from Files.GUI_Modules.Constants import *
from Files.GUI_Modules.Utils import Bind_Hover

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as Plt
import matplotlib.patches as Mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Pie_Overlay:
    def __init__(self, App):
        self.App = App

    def Show(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.destroy()

        self.Overlay_Frame = Tk.Frame(
            self.App.Root,
            bg=Bg_Panel,
            highlightbackground=Accent_Purple,
            highlightthickness=2,
        )
        self.Overlay_Frame.place(relx=0.04, rely=0.04, relwidth=0.92, relheight=0.92)

        Tk.Frame(self.Overlay_Frame, bg=Accent_Purple, height=3).pack(fill=Tk.X)

        Top_Bar = Tk.Frame(self.Overlay_Frame, bg=Bg_Panel)
        Top_Bar.pack(fill=Tk.X, pady=12, padx=20)

        Back_Btn = Tk.Button(
            Top_Bar,
            text="⬅  Back",
            bg=Bg_Card,
            fg=Accent_Purple,
            font=("Segoe UI", 13, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=self.Hide,
            activebackground=Border_Glow,
        )
        Back_Btn.pack(side=Tk.LEFT, ipadx=18, ipady=8)
        Bind_Hover(Back_Btn, Bg_Card, Border_Glow, Accent_Purple, Accent_Gold_Light)

        Tk.Label(
            Top_Bar,
            text="🥧  Balance Distribution",
            bg=Bg_Panel,
            fg=Accent_Purple,
            font=("Segoe UI", 20, "bold"),
        ).pack(side=Tk.LEFT, padx=24)

        Tk.Frame(self.Overlay_Frame, bg=Border_Glow, height=1).pack(fill=Tk.X, padx=20, pady=2)

        self.Chart_Frame = Tk.Frame(self.Overlay_Frame, bg=Bg_Main)
        self.Chart_Frame.pack(pady=12, padx=20, fill=Tk.BOTH, expand=True)

        self.App.Root.update_idletasks()
        self.App.Root.after(80, self.Draw_Chart)

    def Hide(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.place_forget()
            self.Overlay_Frame.destroy()
        try:
            Plt.close("all")
        except Exception:
            pass

    def Draw_Chart(self):
        Label_Sums  = {}
        Label_Order = []
        Current_Label = "Uncategorized"

        for Item in self.App.Dm.Savings:
            if isinstance(Item, str):
                Current_Label = Item.strip()
                if Current_Label not in Label_Sums:
                    Label_Sums[Current_Label] = 0.0
                    Label_Order.append(Current_Label)
            elif isinstance(Item, list):
                if Current_Label not in Label_Sums:
                    Label_Sums[Current_Label] = 0.0
                    Label_Order.append(Current_Label)
                Label_Sums[Current_Label] += float(Item[1])

        Labels = []
        Sizes  = []
        for Lbl in Label_Order:
            Val = round(Label_Sums[Lbl], 2)
            if Val > 0:
                Labels.append(Lbl)
                Sizes.append(Val)

        if not Sizes:
            Tk.Label(self.Chart_Frame, text="No Positive Balances To Display...", bg=Bg_Main, fg=Txt_Muted, font=Font_Lg).pack(expand=True)
            return

        Colors = [
            "#9B59FF", "#00FFEA", "#FFD700", "#39FF14",
            "#FF6B6B", "#5AC8FA", "#FF9500", "#FF2D55",
            "#4CD964", "#AF52DE", "#FFD93D", "#00C7BE",
            "#FF6B35", "#A8FF3E", "#F72585", "#00B4D8",
        ]
        Slice_Colors = [Colors[I % len(Colors)] for I in range(len(Labels))]

        Fig, Ax = Plt.subplots(figsize=(11, 6.5), facecolor=Bg_Panel)
        Ax.set_facecolor(Bg_Panel)

        Explode    = [0.04] * len(Labels)
        Wedge_Props = {"linewidth": 2.5, "edgecolor": Bg_Main}

        Wedges, _, Auto_Texts = Ax.pie(
            Sizes,
            labels=None,
            colors=Slice_Colors,
            autopct=lambda P: f"{P:.1f}%" if P > 5 else "",
            startangle=90,
            wedgeprops=Wedge_Props,
            pctdistance=0.76,
            counterclock=False,
            explode=Explode,
        )

        for At in Auto_Texts:
            At.set_color("#000000")
            At.set_fontsize(9)
            At.set_fontweight("bold")

        Centre_Circle = Plt.Circle((0, 0), 0.52, fc=Bg_Main)
        Ax.add_patch(Centre_Circle)

        Total = sum(Sizes)
        Ax.text(0, 0.08, "Total", ha="center", va="center", fontsize=10, color=Txt_Muted)
        Ax.text(0, -0.12, f"₹{Total:,.2f}", ha="center", va="center", fontsize=14, fontweight="bold", color=Accent_Gold_Light)

        Legend_Patches = []
        for I, Lbl in enumerate(Labels):
            Val = round(Label_Sums[Lbl], 2)
            Pct = (Sizes[I] / Total) * 100
            Patch = Mpatches.Patch(color=Slice_Colors[I], label=f"{Lbl}   ₹{Val:,.2f}  ({Pct:.1f}%)")
            Legend_Patches.append(Patch)

        Legend = Ax.legend(
            handles=Legend_Patches,
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=True,
            facecolor=Bg_Card,
            edgecolor=Accent_Purple,
            labelcolor=Txt_Color,
            fontsize=10,
            title="Categories",
            title_fontsize=12,
        )
        Legend.get_title().set_color(Accent_Purple)

        Ax.set_title("Portfolio Balance Distribution", color=Accent_Purple, fontsize=15, fontweight="bold", pad=14)

        Fig.tight_layout(rect=[0, 0, 0.78, 1])

        Annotation = Ax.annotate(
            "", xy=(0, 0), xytext=(22, 22),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc=Bg_Card, ec=Accent_Purple, alpha=0.94),
            arrowprops=dict(arrowstyle="->", color=Accent_Purple),
            color=Txt_Color, fontsize=11, visible=False,
        )

        def On_Hover(Event):
            Visible = False
            if Event.inaxes == Ax:
                for I, Wedge in enumerate(Wedges):
                    Cont, _ = Wedge.contains(Event)
                    if Cont:
                        Lbl = Labels[I]
                        Val = round(Label_Sums[Lbl], 2)
                        Pct = (Sizes[I] / Total) * 100
                        Annotation.set_text(f"{Lbl}\n₹{Val:,.2f}  ({Pct:.1f}%)")
                        Annotation.xy = (Event.xdata, Event.ydata)
                        Annotation.set_visible(True)
                        Visible = True
                        break
            if not Visible:
                Annotation.set_visible(False)
            Fig.canvas.draw_idle()

        Fig.canvas.mpl_connect("motion_notify_event", On_Hover)

        Canvas_Widget = FigureCanvasTkAgg(Fig, master=self.Chart_Frame)
        Canvas_Widget.draw()
        Canvas_Widget.get_tk_widget().pack(fill=Tk.BOTH, expand=True)
