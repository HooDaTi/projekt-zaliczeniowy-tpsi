import tkinter as tk
import time

root = tk.Tk()

class Cell:
    def __init__(self, occupied = False):
        self.occupied = occupied

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
        self._update_color()   
    
    def _update_color(self):
        self.color = "yellow" if self.state == "A" else "purple"

    def reset(self):
        self.state = "A"
        self._update_color()

    def toggle(self):
        self.state = "B" if self.state == "A" else "A"
        self._update_color()

    def __str__(self):
        return f"Zwrotnica -> {self.state}"


class Station:
    color = "black"

    def __init__(self, position):
        self.position = position




root.title("Automat komórkowy")
root.geometry("1200x800")

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
canvas = tk.Canvas(root, width=900, height=600, bg="white")
canvas.pack(pady=20)

track_rects = []
cell_size = 60
start_x = 100
start_y = 100
positions = []
station1 = Station(position=13)
station2 = Station(position=16)
station3 = Station(position=23)

# gorna krawedz
for i in range(10):
    positions.append((start_x + i*cell_size, start_y))

# prawa krawedz
for i in range(1, 6):
    positions.append((start_x + 9*cell_size, start_y + i*cell_size))

# dolna krawedz
for i in range(1, 10):
    positions.append((start_x + 9*cell_size - i*cell_size, start_y + 5*cell_size))

# lewa krawedz
for i in range(1, 5):
    positions.append((start_x, start_y + 5*cell_size - i*cell_size))

for (x, y) in positions:
    r = canvas.create_rectangle(x, y, x+cell_size, y+cell_size, fill="gray", outline="white")
    track_rects.append(r)


# for i in range(len(track.cells)):
#     x1 = i * cell_size + 5

#     rect = canvas.create_rectangle(x1, 40, x1 + cell_size, 80, fill="gray", outline="white")
#     track_rects.append(rect)

track = Track(len(positions), switch_pos=6)
train = Train(position=0)
first_pos = train.position
step = 0
task_id = None
switch_index = track.switch_pos


track.cells[train.position].occupied = True

x, y = positions[train.position]
train_rect = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="red")
canvas.itemconfig(track_rects[switch_index], fill=track.switch.color)
switch_label = canvas.create_text(start_x + (switch_index * cell_size) + cell_size/2, start_y + cell_size + 5, text=track.switch.state, fill="black")
canvas.itemconfig(track_rects[station1.position], fill=Station.color)
canvas.itemconfig(track_rects[station2.position], fill=Station.color)
canvas.itemconfig(track_rects[station3.position], fill=Station.color)

def update_train_position():
    (x, y) = positions[train.position]
    canvas.coords(train_rect, x, y, x + cell_size, y + cell_size)

def start_movement():
    stop_info.config(text="")
    start_info.config(text="The train has started!", fg="green")
    movement()

def movement():
    global step, task_id

    if step > 50:
        return
    
    if train.position == station1.position or train.position == station2.position or train.position == station3.position:
        stop_movement()
        return
    #zatrzymuje się PRZED peronem, i nie jedzie dalej 
    #zaimplementować aby po paru sekundach ruszał dalej
        
    update_train_position()


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
    track.switch.reset()

    canvas.itemconfig(switch_label, text=track.switch.state)
    canvas.itemconfig(track_rects[switch_index], fill=track.switch.color)
    
    track.cells[train.position].occupied = False
    train.position = first_pos  # początek toru
    track.cells[train.position].occupied = True
    # track_gui.config(text=str(track))
    update_train_position()
    step_count.config(text="Simulation restarted")

def switch():
    track.switch.toggle()
    canvas.itemconfig(switch_label, text=track.switch.state)
    canvas.itemconfig(track_rects[switch_index], fill=track.switch.color)

st_buttons = tk.Frame(root)
st_buttons.pack(pady=10)

start_btn = tk.Button(st_buttons, text="Start", command=start_movement, highlightbackground="green")
stop_btn = tk.Button(st_buttons, text="Stop", command=stop_movement)
restart_btn = tk.Button(st_buttons, text="Reset", command=reset)
switch_btn = tk.Button(st_buttons, text="Switch", command=switch)
start_btn.pack(side="left", padx=5)
stop_btn.pack(side="left", padx=5)
restart_btn.pack(side="left", padx=5)
switch_btn.pack(side="left", padx=5)







root.mainloop()