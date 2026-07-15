import tkinter as Tk
from Files.GUI_Modules.Constants import *
from Files.GUI_Modules.Utils import Bind_Hover

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as Plt
import matplotlib.patches as Mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as Mticker
import numpy as Np

class Graph_Overlay:
    def __init__(self, App):
        self.App = App

    def Show(self):
        if hasattr(self, "Overlay_Frame") and self.Overlay_Frame.winfo_exists():
            self.Overlay_Frame.destroy()

        self.Overlay_Frame = Tk.Frame(
            self.App.Root,
            bg=Bg_Panel,
            highlightbackground=Accent_Cyan_Dark,
            highlightthickness=2,
        )
        self.Overlay_Frame.place(relx=0.04, rely=0.04, relwidth=0.92, relheight=0.92)

        Tk.Frame(self.Overlay_Frame, bg=Accent_Cyan_Dark, height=3).pack(fill=Tk.X)

        Top_Bar = Tk.Frame(self.Overlay_Frame, bg=Bg_Panel)
        Top_Bar.pack(fill=Tk.X, pady=12, padx=20)

        Back_Btn = Tk.Button(
            Top_Bar,
            text="⬅  Back",
            bg=Bg_Card,
            fg=Accent_Cyan,
            font=("Segoe UI", 13, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=self.Hide,
            activebackground=Accent_Cyan_Dark,
        )
        Back_Btn.pack(side=Tk.LEFT, ipadx=18, ipady=8)
        Bind_Hover(Back_Btn, Bg_Card, Border_Glow, Accent_Cyan, Accent_Gold_Light)

        Tk.Label(
            Top_Bar,
            text="📈  Financial Trajectory",
            bg=Bg_Panel,
            fg=Accent_Cyan,
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
        History = self.App.Dm.History
        if not History:
            Tk.Label(self.Chart_Frame, text="No History Data Yet...", bg=Bg_Main, fg=Txt_Muted, font=Font_Lg).pack(expand=True)
            return

        Dates  = list(History.keys())
        Values = self.App.Dm.Get_Hist_Balances()

        if len(Values) < 2:
            First_Val = Values[0] if Values else 0.0
            Tk.Label(
                self.Chart_Frame,
                text=f"Only One Entry: {Dates[0]} — ₹{First_Val:,.2f}\n(Check Back Tomorrow For Graph)",
                bg=Bg_Main, fg=Txt_Muted, font=Font_Main,
            ).pack(expand=True)
            return

        Fig, Ax = Plt.subplots(figsize=(13, 5.5), facecolor=Bg_Panel)
        Ax.set_facecolor(Bg_Main)

        X_Idx    = list(range(len(Values)))
        Smooth_X = Np.linspace(0, len(Values) - 1, 400)
        Smooth_Y = Np.interp(Smooth_X, X_Idx, Values)

        Ax.fill_between(Smooth_X, Smooth_Y, alpha=0.14, color=Accent_Cyan)
        Ax.plot(Smooth_X, Smooth_Y, color=Accent_Cyan, linewidth=2.4, zorder=3)
        Ax.scatter(X_Idx, Values, color=Accent_Gold, s=60, zorder=5, edgecolors=Bg_Panel, linewidths=1.8)

        Annotation = Ax.annotate(
            "", xy=(0, 0), xytext=(16, 16),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc=Bg_Card, ec=Accent_Cyan_Dark, alpha=0.96),
            arrowprops=dict(arrowstyle="->", color=Accent_Cyan_Dark),
            color=Txt_Color, fontsize=11, visible=False,
        )

        def On_Hover(Event):
            if Event.inaxes != Ax or Event.xdata is None:
                Annotation.set_visible(False)
                Fig.canvas.draw_idle()
                return
            Found = False
            for I, (Xp, Yp) in enumerate(zip(X_Idx, Values)):
                if abs(Event.xdata - Xp) < 0.4:
                    Annotation.set_text(f"{Dates[I]}\n₹{float(Yp):,.2f}")
                    Annotation.xy = (Xp, float(Yp))
                    Annotation.set_visible(True)
                    Found = True
                    break
            if not Found:
                Annotation.set_visible(False)
            Fig.canvas.draw_idle()

        Fig.canvas.mpl_connect("motion_notify_event", On_Hover)

        Step = max(1, len(Dates) // 10)
        Ax.set_xticks(X_Idx[::Step])
        Ax.set_xticklabels(Dates[::Step], rotation=35, ha="right", color=Txt_Muted, fontsize=9)

        Ax.yaxis.set_major_formatter(Mticker.FuncFormatter(lambda Val, _: f"₹{Val:,.0f}"))
        Ax.tick_params(colors=Txt_Muted, which="both")

        for Spine in Ax.spines.values():
            Spine.set_edgecolor(Border_Glow)

        Ax.set_title("Balance Over Time", color=Accent_Cyan, fontsize=15, fontweight="bold", pad=14)
        Ax.set_ylabel("Total Balance (₹)", color=Txt_Muted, fontsize=11)
        Ax.grid(True, color=Border_Glow, linestyle="--", linewidth=0.7, alpha=0.6)

        Fig.tight_layout()

        Canvas_Widget = FigureCanvasTkAgg(Fig, master=self.Chart_Frame)
        Canvas_Widget.draw()
        Canvas_Widget.get_tk_widget().pack(fill=Tk.BOTH, expand=True)
