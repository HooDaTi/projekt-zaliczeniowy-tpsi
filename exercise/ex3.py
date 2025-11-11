import time

class Cell:
    def __init__(self, occupied = False):
        self._occupied = occupied

    def toggle(self):
        self._occupied = not self._occupied

    def is_occupied(self):
        return self._occupied

    def __str__(self):
        return "🚂" if self._occupied else "."


class Track:
    def __init__(self, length):
        self._cells = [Cell() for _ in range(length)]

    def place_train(self, pos):
        pos_human = pos - 1
        self._cells[pos_human].toggle()

    def move_train(self, val=1):
        for i in range(len(self._cells)):
            if self._cells[i].is_occupied():
                self._cells[(i + val) % len(self._cells)].toggle()
                self._cells[i].toggle()
                break

    def __str__(self):
        return " ".join(str(cell) for cell in self._cells)


class Train:
    ...


class Switch:
    ...


track = Track(10)
track.place_train(2)

for _ in range(12):
    print("\n" * 10)
    track.move_train()
    print(track)
    time.sleep(1)

