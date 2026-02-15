# ============================================================
# Name: Dossiya Dakou
# Course: EEE 591
# Assignment: Homework 4 (HW-M4)
# Date: February 10, 2026
#
# AI Usage Statement:
# I am a beginner in Python.
# I used AI (ChatGPT) only for conceptual explanations of
# mathematics, modeling, Python syntax, and commenting.
# All code logic and implementation were written and
# fully understood by me.
# Link: https://chatgpt.com/share/e/698b21af-1c18-8004-b336-84e0c8a34dcb
# ============================================================

import sys
import subprocess
import tkinter as tk
from tkinter import ttk

import numpy as np

import matplotlib
# Use a Tkinter-compatible backend so Matplotlib can be embedded in Tkinter
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# -------------------------
# Fixed HW constants
# -------------------------
# These are fixed by the homework instructions (not user inputs)
N = 60   # total number of years simulated
M = 20   # number of Monte Carlo simulation runs


# -------------------------
# Detect OS theme (light/dark)
# -------------------------
def is_dark_mode():
    """
    Best-effort detection of OS dark mode.
    Returns:
        True  -> dark mode detected
        False -> light mode or detection not available
    """
    # Windows: read registry value AppsUseLightTheme (0 = dark, 1 = light)
    if sys.platform.startswith("win"):
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return False  # fallback if registry access fails

    # macOS: "AppleInterfaceStyle" equals "Dark" when dark mode is enabled
    if sys.platform == "darwin":
        try:
            out = subprocess.check_output(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            return out.lower() == "dark"
        except Exception:
            return False  # key usually doesn't exist in light mode

    # Linux/other: no single reliable method here, so default to light mode
    return False


# -------------------------
# Simulation (one run)
# -------------------------
def simulate_one_run(r, sigma, Y, C, R, S):
    """
    Run ONE Monte Carlo simulation of wealth over N years.

    Inputs:
        r     : mean annual return (%) e.g., 6 means 6%
        sigma : std dev of annual return (%) e.g., 20 means 20%
        Y     : yearly contribution ($) during contribution years
        C     : number of years of contribution (integer)
        R     : retirement year (integer, 0..N) -- retirement wealth is W[R]
        S     : annual spending in retirement ($) during retirement years

    Returns:
        x     : year indices for plotting (0..end)
        y     : wealth values for plotting (W[0]..W[end])
        w_ret : wealth at retirement year W[R] (or 0 if wealth ended before R)
    """

    # Required noise model: sigma/100 * randn(N)
    # This creates one random return "shock" per year for N years.
    noise = (sigma / 100.0) * np.random.randn(N)

    # Wealth array W[0..N], starting from W[0] = 0
    W = np.zeros(N + 1, dtype=float)

    # If wealth hits zero, we record the year and stop early
    run_out = None

    # Update wealth year-by-year: compute W[i+1] from W[i]
    for i in range(N):
        # Growth factor for this year: 1 + mean return + noise
        g = 1.0 + (r / 100.0) + noise[i]

        # Phase 1 (contribution years): i < C
        if i < C:
            W[i + 1] = W[i] * g + Y

        # Phase 2 (working, no contributions): C <= i < R
        elif i < R:
            W[i + 1] = W[i] * g

        # Phase 3 (retirement withdrawals): i >= R
        # Important: withdrawals affect W[R+1] first, so retirement wealth is W[R]
        else:
            W[i + 1] = W[i] * g - S

        # Enforce non-negativity: if wealth becomes <= 0, clamp to 0 and stop
        if W[i + 1] <= 0.0:
            W[i + 1] = 0.0
            run_out = i + 1
            break

    # Build x/y arrays for plotting:
    # - If wealth never ran out: plot full years 0..N
    # - If wealth ran out early: plot only up to run_out
    if run_out is None:
        x = np.arange(N + 1)
        y = W
    else:
        x = np.arange(run_out + 1)
        y = W[: run_out + 1]

    # Retirement wealth is W[R]. If the run ended before R, retirement wealth is 0.
    w_ret = 0.0 if (run_out is not None and run_out < R) else W[R]

    return x, y, w_ret


# -------------------------
# Monte Carlo (M runs)
# -------------------------
def run_monte_carlo(r, sigma, Y, C, R, S):
    """
    Run the simulation M times to capture randomness across runs.

    Returns:
        avg_ret : average retirement wealth over the M runs
        all_x   : list of x arrays (one per run) for plotting
        all_y   : list of y arrays (one per run) for plotting
    """
    all_x, all_y, wrets = [], [], []

    for _ in range(M):
        x, y, wret = simulate_one_run(r, sigma, Y, C, R, S)
        all_x.append(x)      # store x-axis for this run
        all_y.append(y)      # store wealth curve for this run
        wrets.append(wret)   # store wealth at retirement for averaging

    avg_ret = float(np.mean(wrets))
    return avg_ret, all_x, all_y


# ============================================================
# GUI
# ============================================================

# Create the main Tkinter window
root = tk.Tk()
root.title("HW4 (HW-M4) - Retirement Wealth Simulator")
root.geometry("1180x700")

# Detect system theme so UI can match light/dark mode
dark = is_dark_mode()

# Color palettes for light/dark mode (visual only; does not affect simulation)
PALETTES = {
    True: dict(   # dark theme colors
        BG="#0f172a", TEXT="#e5e7eb", MUTED="#94a3b8",
        ACCENT="#3b82f6", DANGER="#ef4444",
        ENTRY_BG="#ffffff", ENTRY_FG="#111827",
        PLOT_BG="#0b1220", SPINE="#334155",
        ACTIVE_PRIMARY="#2563eb", ACTIVE_DANGER="#dc2626"
    ),
    False: dict(  # light theme colors
        BG="#f3f4f6", TEXT="#111827", MUTED="#4b5563",
        ACCENT="#2563eb", DANGER="#dc2626",
        ENTRY_BG="#ffffff", ENTRY_FG="#111827",
        PLOT_BG="#ffffff", SPINE="#cbd5e1",
        ACTIVE_PRIMARY="#1d4ed8", ACTIVE_DANGER="#b91c1c"
    )
}

colors = PALETTES[dark]
root.configure(bg=colors["BG"])  # affects tk widgets + window background


# -------------------------
# ttk styles
# -------------------------
# ttk widgets use a "Style" object for consistent appearance
style = ttk.Style()

# Use a common theme that works well on many systems, if available
if "clam" in style.theme_names():
    style.theme_use("clam")

# Default font applied widely across ttk widgets
style.configure(".", font=("Segoe UI", 11))

# Base styles
style.configure("TFrame", background=colors["BG"])
style.configure("TLabel", background=colors["BG"], foreground=colors["TEXT"])
style.configure("Muted.TLabel", background=colors["BG"], foreground=colors["MUTED"])

# LabelFrame border area + its title label
style.configure("TLabelframe", background=colors["BG"], foreground=colors["TEXT"])
style.configure(
    "TLabelframe.Label",
    background=colors["BG"],
    foreground=colors["TEXT"],
    font=("Segoe UI", 11, "bold")
)

# Entry appearance (fieldbackground controls the text box interior)
style.configure("TEntry", fieldbackground=colors["ENTRY_BG"], foreground=colors["ENTRY_FG"])

# Default button styling
style.configure("TButton", padding=(10, 6), font=("Segoe UI", 11, "bold"))

# Custom "Primary" style for Calculate button
style.configure("Primary.TButton", background=colors["ACCENT"], foreground="#ffffff")
style.map("Primary.TButton", background=[("active", colors["ACTIVE_PRIMARY"])])

# Custom "Danger" style for Quit button
style.configure("Danger.TButton", background=colors["DANGER"], foreground="#ffffff")
style.map("Danger.TButton", background=[("active", colors["ACTIVE_DANGER"])])


# -------------------------
# Layout containers
# -------------------------
# Configure the root grid so the main frame expands with the window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Main container: left controls + right plot
main = ttk.Frame(root, padding=12)
main.grid(row=0, column=0, sticky="nsew")

# Left side stays compact; right side expands for the plot
main.columnconfigure(0, weight=0)
main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=1)

# ---- Left: Controls ----
controls = ttk.LabelFrame(main, text="Inputs", padding=12)
controls.grid(row=0, column=0, sticky="nsw", padx=(0, 12), pady=6)
controls.columnconfigure(0, weight=1)
controls.columnconfigure(1, weight=1)

def add_field(row, label, default):
    """Create one label + entry row and return the Entry widget."""
    ttk.Label(controls, text=label, style="Muted.TLabel").grid(
        row=row, column=0, sticky="w", pady=7
    )
    ent = ttk.Entry(controls, width=22)
    ent.grid(row=row, column=1, sticky="ew", pady=7)
    ent.insert(0, default)
    return ent

# Input fields (defaults are example values; user may change them)
e_mean = add_field(0, "Mean Return (%)", "6")
e_std  = add_field(1, "Std Dev Return (%)", "20")
e_Y    = add_field(2, "Yearly Contribution ($)", "10000")
e_C    = add_field(3, "No. Years of Contribution", "30")
e_R    = add_field(4, "No. Years to Retirement", "40")
e_S    = add_field(5, "Annual Spend in Retirement ($)", "80000")

# Label that displays output (HW requirement: show average retirement wealth)
result_var = tk.StringVar(value="Wealth at retirement (avg):")
result_label = ttk.Label(controls, textvariable=result_var, wraplength=360)
result_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(16, 6))
result_label.configure(font=("Segoe UI", 12, "bold"))

# Buttons container
btns = ttk.Frame(controls)
btns.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))
btns.columnconfigure(0, weight=1)
btns.columnconfigure(1, weight=1)

# ---- Right: Plot ----
plot_frame = ttk.LabelFrame(main, text="Simulation Plot", padding=8)
plot_frame.grid(row=0, column=1, sticky="nsew", pady=6)
plot_frame.columnconfigure(0, weight=1)
plot_frame.rowconfigure(0, weight=1)
plot_frame.rowconfigure(1, weight=0)

# Matplotlib figure + axis (embedded into Tkinter)
fig = Figure(figsize=(7.8, 5.4), dpi=100)
fig.patch.set_facecolor(colors["PLOT_BG"])
ax = fig.add_subplot(111)

def style_axes():
    """Apply consistent formatting to the axes (call after ax.clear())."""
    ax.set_facecolor(colors["PLOT_BG"])
    ax.set_title(f"Wealth vs Year ({M} runs, N={N})", color=colors["TEXT"])
    ax.set_xlabel("Year", color=colors["TEXT"])
    ax.set_ylabel("Wealth ($)", color=colors["TEXT"])
    ax.tick_params(colors=colors["TEXT"])
    for sp in ax.spines.values():
        sp.set_color(colors["SPINE"])
    ax.grid(True, alpha=0.25)

style_axes()

# Create and place the embedded canvas widget
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# Toolbar note:
# NavigationToolbar2Tk uses pack() internally, so we place it in a dedicated frame
# to avoid mixing pack() and grid() in the SAME parent widget.
toolbar_frame = ttk.Frame(plot_frame)
toolbar_frame.grid(row=1, column=0, sticky="ew")
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

def show_error(msg):
    """Display an error message in red in the output label."""
    result_label.configure(foreground=colors["DANGER"])
    result_var.set(msg)

def show_ok(msg):
    """Display a normal (success) message in the output label."""
    result_label.configure(foreground=colors["TEXT"])
    result_var.set(msg)

def on_calculate():
    """
    Calculate button callback:
      1) read + convert inputs
      2) validate inputs
      3) run Monte Carlo simulation
      4) update the label and plot
    """
    # Convert Entry strings to numbers
    try:
        r = float(e_mean.get())
        sigma = float(e_std.get())
        Y = float(e_Y.get())
        Cyears = int(float(e_C.get()))
        Ryears = int(float(e_R.get()))
        S = float(e_S.get())
    except ValueError:
        show_error("Error: Please enter valid numeric values in all fields.")
        return

    # Basic input validation
    if sigma < 0:
        show_error("Error: Std Dev (%) must be >= 0.")
        return
    if Cyears < 0:
        show_error("Error: No. Years of Contribution must be >= 0.")
        return
    if Ryears < 0 or Ryears > N:
        show_error(f"Error: No. Years to Retirement must be between 0 and {N}.")
        return

    # HW rule: contributions cannot continue after retirement
    Cyears = min(Cyears, Ryears)

    # Run the Monte Carlo simulation
    avg_ret, all_x, all_y = run_monte_carlo(r, sigma, Y, Cyears, Ryears, S)

    # Update required output label
    show_ok(f"Wealth at retirement (avg of {M} runs): ${avg_ret:,.0f}")

    # Redraw plot for this run: clear old curves, restyle, then plot new curves
    ax.clear()
    style_axes()
    for x, y in zip(all_x, all_y):
        ax.plot(x, y)
    canvas.draw()

# Create buttons (note: command points to functions, not function calls)
ttk.Button(btns, text="Quit", command=root.destroy, style="Danger.TButton").grid(
    row=0, column=0, sticky="ew", padx=(0, 6)
)
ttk.Button(btns, text="Calculate", command=on_calculate, style="Primary.TButton").grid(
    row=0, column=1, sticky="ew", padx=(6, 0)
)

# Start the Tkinter event loop (keeps the GUI running)
root.mainloop()
