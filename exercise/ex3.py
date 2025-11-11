import time

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
        self._direction = direction # 1 = w prawo, -1 = w lewo

    def move(self, track_length, track):
        if track.switch_pos == self.position:
            if track.switch.state == "B":
                self._direction *= -1
                print("🚦 Zwrotnica zmieniła kierunek jazdy!")
        
        self.position = (self.position + self._direction) % track_length


class Switch:
    def __init__(self):
        self.state =  "A" # "A" = prosto, "B" = skręt

    def toggle(self):
        self.state = "B" if self.state == "A" else "A"

    def __str__(self):
        return f"Zwrotnica -> {self.state}"


track = Track(length=10, switch_pos=4)
train = Train(position=2)
track.cells[train.position].occupied = True

for step in range(15):
    print("\n" * 8)
    print(f"Krok {step}")
    print(track)
    time.sleep(1)

    track.cells[train.position].occupied = False
    train.move(len(track.cells), track)
    track.cells[train.position].occupied = True

    if step == 11:
        print("🔁 Zmieniam zwrotnicę!")
        track.switch.toggle()