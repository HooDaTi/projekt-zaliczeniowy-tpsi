import tkinter as tk
import time

root = tk.Tk()
root.title("To jest GUI")
root.geometry("1000x500")
####################################
label = tk.Label(root, text="Czekam na start...", fg="blue")
label.pack(pady=20)

def update_label():
    label.config(text="Pociąg ruszył! 🚂", bg="yellow")

button = tk.Button(root, text="Start", command=update_label, fg="red", bg="green")
button.pack()
####################################
frame = tk.Frame(root)
frame.pack()

start_btn = tk.Button(frame, text="Start")
pause_btn = tk.Button(frame, text="Pauza")

start_btn.pack(side="left", padx=5)
pause_btn.pack(side="left", padx=5)
###########################################
canvas = tk.Canvas(root, width=400, height=200, bg="lightgray")
canvas.pack()

# Rysowanie prostokąta (x1, y1, x2, y2)
canvas.create_rectangle(50, 80, 100, 120, fill="red")

# Rysowanie kółka
canvas.create_oval(150, 80, 200, 130, fill="blue")

# Rysowanie tekstu
canvas.create_text(100, 50, text="Pociąg", font=("Arial", 14))
##############################################
def update():
    label.config(text=time.strftime("%H:%M:%S"))
    root.after(2000, update)

update()




























root.mainloop()