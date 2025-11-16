import tkinter as tk
import time

root = tk.Tk()

class Cell:
    def __init__(self, occupied = False):
        self.occupied = occupied

    # def toggle(self):
    #     self.occupied = not self.occupied

    def is_occupied(self):
        return self.occupied
    
    def set_occupied(self, value: bool):
        self.occupied = value

    def __str__(self):
        return "🚂" if self.occupied else "."


class Track:
    def __init__(self, length, switch_pos=None):
        self.cells = [Cell() for _ in range(length)]
        self.switch_pos = switch_pos
        self.switch = Switch() if switch_pos is not None else None

    def __str__(self):
        result = []
        for i, cell in enumerate(self.cells):
            if self.switch_pos == i:
                result.append("🔀")
            else:
                result.append(str(cell))
        return " ".join(result)


class Train:
    def __init__(self, position=0, direction=1):
        self.position = position # aktualna pozycja pociągu
        self.direction = direction # 1 = w prawo, -1 = w lewo

    def move(self, track_length, track):
        if track.switch_pos == self.position:
            if track.switch.state == "B":
                self.direction *= -1
                print("🚦 Zwrotnica zmieniła kierunek jazdy!")
        
        self.position = (self.position + self.direction) % track_length


class Switch:
    def __init__(self):
        self.state =  "A" # "A" = prosto, "B" = skręt

    def toggle(self):
        self.state = "B" if self.state == "A" else "A"

    def __str__(self):
        return f"Zwrotnica -> {self.state}"


track = Track(length=9, switch_pos=6)
train = Train(position=1)
step = 0
task_id = None
root.title("Automat komórkowy")
root.geometry("1000x500")

track.cells[train.position].occupied = True

info = tk.Frame(root)
info.pack()

start_info = tk.Label(info, text="")
start_info.pack(side="top")
stop_info = tk.Label(info, text="")
stop_info.pack(side="top")
step_count = tk.Label(info, text="", fg="red")
step_count.pack(side="top")
'''
# track_gui = tk.Label(root, text=str(track))
# track_gui.pack()
'''
canvas = tk.Canvas(root, width=600, height=100, bg="white")
canvas.pack(pady=20)

cell_size = 60
track_rects = []

for i in range(len(track.cells)):
    x1 = i * cell_size
    rect = canvas.create_rectangle(x1, 40, x1 + cell_size, 80, fill="gray", outline="white")
    track_rects.append(rect)
train_rect = canvas.create_rectangle(train.position * cell_size, 30, (train.position * cell_size) + cell_size, 90, fill="red")
switch_rect = canvas.create_rectangle(track.switch_pos * cell_size, 40, (track.switch_pos * cell_size) + cell_size, 80, fill="purple")

def update_train_position():
    x = train.position * cell_size
    canvas.coords(train_rect, x, 30, x + cell_size, 90)

def start_movement():
    stop_info.config(text="")
    start_info.config(text="The train has started!", fg="green")
    movement()

def movement():
    global step, task_id

    update_train_position()

    if step >= 15:
        return
    
    step_count.config(text=f"Current step: {step}")
    track.cells[train.position].occupied = False
    train.move(len(track.cells), track)
    track.cells[train.position].occupied = True
    
    step += 1
    task_id = root.after(1000, movement)

def stop_movement():
    if task_id:
        root.after_cancel(task_id)

    start_info.config(text="")
    stop_info.config(text="The train has stopped!", fg="red")

def reset():
    global step

    if task_id:
        root.after_cancel(task_id)
    step = 0
    start_info.config(text="")
    stop_info.config(text="")
    train.direction = 1
    
    track.cells[train.position].occupied = False
    train.position = 1  # np. początek toru
    track.cells[train.position].occupied = True
    # track_gui.config(text=str(track))
    update_train_position()
    step_count.config(text="Simulation restarted")

def switch():
    track.switch.toggle()
    stop_info.config(text=f"Switch changed to {track.switch.state} state!")

st_buttons = tk.Frame(root)
st_buttons.pack(pady=10)

start_btn = tk.Button(st_buttons, text="Start", command=start_movement)
stop_btn = tk.Button(st_buttons, text="Stop", command=stop_movement)
restart_btn = tk.Button(st_buttons, text="Reset", command=reset)
switch_btn = tk.Button(st_buttons, text="Switch", command=switch)
start_btn.pack(side="left", padx=5)
stop_btn.pack(side="left", padx=5)
restart_btn.pack(side="left", padx=5)
switch_btn.pack(side="left", padx=5)







root.mainloop()