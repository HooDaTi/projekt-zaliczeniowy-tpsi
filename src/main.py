import tkinter as tk
from tkinter import ttk

# Konfiguracja stałych
CELL_SIZE = 60
START_X = 100
START_Y = 70
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BG_COLOR = "#2e2e2e"  
TRACK_COLOR = "#7f8c8d" 

class Cell:
    def __init__(self, occupied: bool = False):
        self.occupied = occupied

    def is_occupied(self) -> bool:
        return self.occupied
    
    def set_occupied(self, value: bool) -> None:
        self.occupied = value

    def __str__(self):
        return "🚂" if self.occupied else "."

class Switch:
    def __init__(self):
        self.state =  "A" # "A" = prosto, "B" = skręt
        self._update_color()   
    
    def _update_color(self) -> None:
        self.color = "#f1c40f" if self.state == "A" else "#8e44ad"

    def reset(self) -> None:
        self.state = "A"
        self._update_color()

    def toggle(self) -> None:
        self.state = "B" if self.state == "A" else "A"
        self._update_color()

class Station:
    color = "#2c3e50"
    def __init__(self, position: int):
        self.position = position

class Track:
    def __init__(self, length: int, switch_pos: int = None):
        self.cells = [Cell() for _ in range(length)]
        self.switch_pos = switch_pos
        self.switch = Switch() if switch_pos is not None else None
        self.junctions = {}
        self.forced_next = {}

class Train:
    def __init__(self, position: int = 0, direction: int = 1):
        self.position = position
        self.direction = direction

    def move(self, track: 'Track') -> None:
        pos = self.position
        if pos in track.junctions:
            self.position = track.junctions[pos][track.switch.state]
            return
        if pos in track.forced_next:
            self.position = track.forced_next[pos]
            return
        self.position = (pos + self.direction) % len(track.cells)

class SimulationApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automat komórkowy")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=BG_COLOR)

        self.step = 0
        self.task_id = None
        self.is_running = False

        self.setup_logic()

        self.setup_gui()

        self.refresh_gui()

    def setup_logic(self):
        self.positions = []
        self.track_rects = []

        # Gorna
        for i in range(10):
            self.positions.append((START_X + i*CELL_SIZE, START_Y))
        # Prawa
        for i in range(1, 6):
            self.positions.append((START_X + 9*CELL_SIZE, START_Y + i*CELL_SIZE))
        # Dolna
        for i in range(1, 10):
            self.positions.append((START_X + 9*CELL_SIZE - i*CELL_SIZE, START_Y + 5*CELL_SIZE))
        # Lewa
        for i in range(1, 5):
            self.positions.append((START_X, START_Y + 5*CELL_SIZE - i*CELL_SIZE))

        self.branch_positions = {
            28: (START_X + 6*CELL_SIZE, START_Y + CELL_SIZE),
            29: (START_X + 6*CELL_SIZE, START_Y + 2*CELL_SIZE),
            30: (START_X + 7*CELL_SIZE, START_Y + 2*CELL_SIZE),
            31: (START_X + 8*CELL_SIZE, START_Y + 2*CELL_SIZE),
        }

        total_len = len(self.positions) + len(self.branch_positions)
        self.track = Track(total_len, switch_pos=6)
        self.train = Train(position=0)
        self.first_pos = self.train.position

        self.station1 = Station(position=8)
        self.station2 = Station(position=29)
        self.station3 = Station(position=25)
        self.stations = [self.station1, self.station2, self.station3]

        self.track.junctions[6] = {"A" : 7, "B" : 28}
        self.track.forced_next[28] = 29
        self.track.forced_next[29] = 30
        self.track.forced_next[30] = 31
        self.track.forced_next[31] = 11 
        self.track.forced_next[27] = 0

        self.track.cells[self.train.position].occupied = True

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TButton", font=('Helvetica', 10, 'bold'), padding=6)

        self.info_frame = tk.Frame(self, bg=BG_COLOR)
        self.info_frame.pack(pady=10)

        self.status_label = tk.Label(self.info_frame, text="Gotowy do startu", font=("Arial", 14), fg="white", bg=BG_COLOR)
        self.status_label.pack()
        
        self.step_label = tk.Label(self.info_frame, text="Krok: 0", font=("Arial", 10), fg="#bdc3c7", bg=BG_COLOR)
        self.step_label.pack()

        self.canvas = tk.Canvas(self, width=800, height=500, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=20)

        for (x, y) in self.positions:
            r = self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill=TRACK_COLOR, outline="white", width=2)
            self.track_rects.append(r)

        for idx in sorted(self.branch_positions.keys()):
            (x, y) = self.branch_positions[idx]
            r = self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill=TRACK_COLOR, outline="white", width=2)
            self.track_rects.append(r)

        sw_x = START_X + (self.track.switch_pos * CELL_SIZE) + CELL_SIZE/2
        sw_y = START_Y - 15
        self.switch_label = self.canvas.create_text(sw_x, sw_y, text=self.track.switch.state, fill="white", font=("Arial", 12, "bold"))

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Start", command=self.start_movement).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Stop", command=self.stop_movement).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Przełącz Zwrotnicę", command=self.switch).pack(side="left", padx=20)

    def refresh_gui(self):
        for i, cell in enumerate(self.track.cells):
            color = TRACK_COLOR
            if cell.is_occupied():
                color = "#e74c3c" # Pociąg
            elif any(s.position == i for s in self.stations): 
                color = Station.color
            elif i == self.track.switch_pos:
                color = self.track.switch.color
        
            self.canvas.itemconfig(self.track_rects[i], fill=color)

        self.step_label.config(text=f"Krok: {self.step}")
        self.canvas.itemconfig(self.switch_label, text=self.track.switch.state)

    def movement(self):
        if self.step > 100:
            return
        
        self.step += 1

        self.track.cells[self.train.position].occupied = False
        self.train.move(self.track)
        self.track.cells[self.train.position].occupied = True
        self.refresh_gui()

        if any(self.train.position == s.position for s in self.stations):
            self.status_label.config(text="Pociąg stoi na stacji", fg="#13b0c5")
            self.task_id = self.after(2000, self.movement)
        else:
            self.status_label.config(text="Pociąg w ruchu...", fg="#14ff62")
            self.task_id = self.after(500, self.movement)

    def start_movement(self):
        if not self.is_running:
            self.is_running = True
            self.movement()

    def stop_movement(self):
        if self.task_id:
            self.after_cancel(self.task_id)
            self.task_id = None
        self.is_running = False
        self.status_label.config(text="Symulacja zatrzymana", fg="#ad123c")

    def reset(self):
        self.stop_movement()
        self.step = 0
        self.train.direction = 1
        self.track.switch.reset()
        self.status_label.config(text="Zresetowano", fg="#ffffff")

        self.track.cells[self.train.position].occupied = False
        self.train.position = self.first_pos
        self.track.cells[self.train.position].occupied = True

        self.refresh_gui()

    def switch(self):
        self.track.switch.toggle()
        self.refresh_gui()


if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()