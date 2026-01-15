import tkinter as tk

root = tk.Tk()

class Cell:
    def __init__(self, occupied: bool = False):
        self.occupied = occupied

    def is_occupied(self) -> bool:
        return self.occupied
    
    def set_occupied(self, value: bool) -> None:
        self.occupied = value

    def __str__(self):
        return "🚂" if self.occupied else "."


class Track:
    def __init__(self, length: int, switch_pos: int = None):
        self.cells = [Cell() for _ in range(length)]
        self.switch_pos = switch_pos
        self.switch = Switch() if switch_pos is not None else None

        # Rozwidlenia
        self.junctions = {}   # { position: {"A": next, "B": next} }
        self.forced_next = {} # { position: next }
        
    def __str__(self):
        result = []
        for i, cell in enumerate(self.cells):
            if self.switch_pos == i:
                result.append("🔀")
            else:
                result.append(str(cell))
        return " ".join(result)


class Train:
    def __init__(self, position: int = 0, direction: int = 1):
        self.position = position # Aktualna pozycja pociągu
        self.direction = direction # 1 = w prawo, -1 = w lewo

    def move(self, track: 'Track') -> None:
        pos = self.position
        
        if pos in track.junctions:
            self.position = track.junctions[pos][track.switch.state]
            return
        
        if pos in track.forced_next:
            self.position = track.forced_next[pos]
            return
        
        self.position = (pos + self.direction) % len(track.cells)

class Switch:
    def __init__(self):
        self.state =  "A" # "A" = prosto, "B" = skręt
        self._update_color()   
    
    def _update_color(self) -> None:
        self.color = "yellow" if self.state == "A" else "purple"

    def reset(self) -> None:
        self.state = "A"
        self._update_color()

    def toggle(self) -> None:
        self.state = "B" if self.state == "A" else "A"
        self._update_color()

    def __str__(self):
        return f"Zwrotnica -> {self.state}"


class Station:
    color = "black"

    def __init__(self, position: int):
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
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack(pady=20)
canvas.config(background="lightgrey")

cell_size = 60
start_x = 100
start_y = 70

track_rects = []
positions = []
branch_positions = {
    28: (start_x + 6*cell_size, start_y + cell_size),
    29: (start_x + 6*cell_size, start_y + 2*cell_size),
    30: (start_x + 7*cell_size, start_y + 2*cell_size),
    31: (start_x + 8*cell_size, start_y + 2*cell_size),
}
station1 = Station(position=8)
station2 = Station(position=29)
station3 = Station(position=25)


# Gorna krawedz
for i in range(10):
    positions.append((start_x + i*cell_size, start_y))

# Prawa krawedz
for i in range(1, 6):
    positions.append((start_x + 9*cell_size, start_y + i*cell_size))

# Dolna krawedz
for i in range(1, 10):
    positions.append((start_x + 9*cell_size - i*cell_size, start_y + 5*cell_size))

# Lewa krawedz
for i in range(1, 5):
    positions.append((start_x, start_y + 5*cell_size - i*cell_size))

for (x, y) in positions:
    r = canvas.create_rectangle(x, y, x+cell_size, y+cell_size, fill="gray", outline="white")
    track_rects.append(r)

for idx in sorted(branch_positions.keys()):
    (x, y) = branch_positions[idx]
    r = canvas.create_rectangle(x, y, x+cell_size, y+cell_size, fill="lightgray", outline="white")
    track_rects.append(r)

# Tworzenie toru
total_len = len(positions) + len(branch_positions)

track = Track(total_len, switch_pos=6)

# Dodanie pociągu
train = Train(position=0)

# Pierwsza pozycja pociągu (Do resetu)
first_pos = train.position

# Inicjalizacja zmiennych
step = 0
task_id = None

# Przypisanie zwrotnicy do zmiennej
switch_index = track.switch_pos

# Rozwidlenie w 6
track.junctions[6] = {
    "A" : 7, # Główny tor
    "B" : 28 # Boczny tor
}

# Boczny tor
track.forced_next[28] = 29
track.forced_next[29] = 30
track.forced_next[30] = 31
track.forced_next[31] = 11  # Powrót na główny tor

# Zataczanie normalnej pętli
track.forced_next[27] = 0


track.cells[train.position].occupied = True

x, y = positions[train.position]

switch_label = canvas.create_text(start_x + (switch_index * cell_size) + cell_size/2, start_y - 5, text=track.switch.state, fill="white")

def refresh_gui():
    for i, cell in enumerate(track.cells):
        color = "gray" 
        if cell.is_occupied():
            color = "red"  # Pociąg
        elif i == station1.position or i == station2.position or i == station3.position: 
            color = Station.color
        elif i == track.switch_pos:
            color = track.switch.color
        canvas.itemconfig(track_rects[i], fill=color)

    stop_info.config(text="")

refresh_gui()

def start_movement():
    stop_info.config(text="")
    start_info.config(text="The train has started!", fg="green")
    movement()

def movement():
    global step, task_id

    if step > 50:
        return
    
    step += 1
    step_count.config(text=f"Current step: {step}")
    track.cells[train.position].occupied = False
    train.move(track)
    track.cells[train.position].occupied = True

    refresh_gui()
    stations = [station1, station2, station3]
    if any(train.position == s.position for s in stations):
        task_id = root.after(4500, movement)
        stop_info.config(text="The train is on the station", fg="blue", bg="yellow")
    else:
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
    train.position = first_pos  # Początek toru (Pierwsza pozycja pociągu)
    track.cells[train.position].occupied = True

    refresh_gui()

    step_count.config(text="Simulation restarted")

def switch():
    track.switch.toggle()
    canvas.itemconfig(switch_label, text=track.switch.state)
    canvas.itemconfig(track_rects[switch_index], fill=track.switch.color)

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