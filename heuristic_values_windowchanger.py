import tkinter as tk

def change_heuristic_values(weights_editable, on_update=None):
    
    weight_names = [
        "Aggregate Height",
        "Cleared Lines",
        "Bumpiness",
        "Blockade",
        "Tetris Well",
        "I Piece Dependencies",
        "Holes",
        "PC Bonus",
        "Extra Weight I",
        "Extra Weight J",
        "Extra Weight K",
    ]

    if len(weights_editable) < len(weight_names):
        weights_editable.extend([0.0] * (len(weight_names) - len(weights_editable)))

    root = tk.Tk()
    root.title("Heuristic Weights")
    root.geometry("500x400")

    for i, name in enumerate(weight_names):
        frame = tk.Frame(root)
        frame.pack(fill=tk.X, padx=10, pady=5)

        label = tk.Label(frame, text=name, width=25, anchor="w")
        label.pack(side=tk.LEFT)

        value_label = tk.Label(frame, text=f"{weights_editable[i]:.2f}", width=8)
        value_label.pack(side=tk.LEFT, padx=5)

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(side=tk.LEFT, padx=5)

        def update_and_refresh(idx, delta, val_lbl):
            weights_editable[idx] += delta
            val_lbl.config(text=f"{weights_editable[idx]:.2f}")
            if on_update is not None:
                on_update()

        tk.Button(buttons_frame, text="-", width=3, command=lambda idx=i, vl=value_label: update_and_refresh(idx, -0.1, vl)).grid(row=0, column=0, padx=2)
        tk.Button(buttons_frame, text="+", width=3, command=lambda idx=i, vl=value_label: update_and_refresh(idx, 0.1, vl)).grid(row=0, column=1, padx=2)

        tk.Button(buttons_frame, text="-", width=3, command=lambda idx=i, vl=value_label: update_and_refresh(idx, -1, vl)).grid(row=0, column=2, padx=6)
        tk.Button(buttons_frame, text="+", width=3, command=lambda idx=i, vl=value_label: update_and_refresh(idx, 1, vl)).grid(row=0, column=3, padx=2)

    root.mainloop()
    return weights_editable

if __name__ == "__main__":
    import heuristic
    change_heuristic_values(heuristic.weights_editable)