import tkinter as tk

def tk_color_picker(initial_color=(255, 255, 255), initial_thickness=1, prompt="Elija color y grosor", show_thickness=True):
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    win = tk.Toplevel()
    win.title(prompt)
    win.resizable(False, False)
    # Ajusta la geometría según si se muestra el slider de grosor o no.
    if show_thickness:
        win.geometry("400x600")
    else:
        win.geometry("400x550")

    result = {"color": None, "thickness": None}

    def cancel():
        result["color"] = None
        result["thickness"] = None
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", cancel)

    # Zona de previsualización: ocupa la mitad superior con padding adicional
    preview_frame = tk.Frame(win, bg="#%02x%02x%02x" % initial_color, width=400, height=250, relief="solid", bd=2)
    preview_frame.pack(fill="x", padx=20, pady=20)

    controls_frame = tk.Frame(win)
    controls_frame.pack(fill="both", expand=True, padx=20, pady=10)

    r_var = tk.IntVar(value=initial_color[0])
    g_var = tk.IntVar(value=initial_color[1])
    b_var = tk.IntVar(value=initial_color[2])
    thickness_var = tk.IntVar(value=initial_thickness)

    def update_preview(*args):
        color = (r_var.get(), g_var.get(), b_var.get())
        hex_color = "#%02x%02x%02x" % color
        preview_frame.config(bg=hex_color)
        r_label.config(text=f"R: {r_var.get()}")
        g_label.config(text=f"G: {g_var.get()}")
        b_label.config(text=f"B: {b_var.get()}")
        if show_thickness and thickness_label:
            thickness_label.config(text=f"Grosor: {thickness_var.get()} px")

    r_var.trace("w", update_preview)
    g_var.trace("w", update_preview)
    b_var.trace("w", update_preview)
    thickness_var.trace("w", update_preview)

    r_label = tk.Label(controls_frame, text=f"R: {r_var.get()}")
    r_label.pack(anchor="w")
    r_scale = tk.Scale(controls_frame, from_=0, to=255, orient="horizontal", variable=r_var)
    r_scale.pack(fill="x")

    g_label = tk.Label(controls_frame, text=f"G: {g_var.get()}")
    g_label.pack(anchor="w")
    g_scale = tk.Scale(controls_frame, from_=0, to=255, orient="horizontal", variable=g_var)
    g_scale.pack(fill="x")

    b_label = tk.Label(controls_frame, text=f"B: {b_var.get()}")
    b_label.pack(anchor="w")
    b_scale = tk.Scale(controls_frame, from_=0, to=255, orient="horizontal", variable=b_var)
    b_scale.pack(fill="x")

    thickness_label = None
    thickness_scale = None
    if show_thickness:
        thickness_label = tk.Label(controls_frame, text=f"Grosor: {thickness_var.get()} px")
        thickness_label.pack(anchor="w")
        thickness_scale = tk.Scale(controls_frame, from_=1, to=100, orient="horizontal", variable=thickness_var)
        thickness_scale.pack(fill="x")

    button_frame = tk.Frame(controls_frame)
    button_frame.pack(pady=10)

    def accept():
        result["color"] = (r_var.get(), g_var.get(), b_var.get())
        result["thickness"] = thickness_var.get() if show_thickness else None
        win.destroy()

    cancel_button = tk.Button(button_frame, text="Cancelar", command=cancel)
    cancel_button.pack(side="left", padx=10)
    accept_button = tk.Button(button_frame, text="Aceptar", command=accept)
    accept_button.pack(side="right", padx=10)

    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_reqwidth()) // 2
    y = (win.winfo_screenheight() - win.winfo_reqheight()) // 2
    win.geometry(f"+{x}+{y}")

    win.grab_set()
    win.wait_window()
    root.destroy()
    return result["color"], result["thickness"]
