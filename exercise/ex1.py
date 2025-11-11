import time

track = ['.', '.', '🚂', '.', '.', '.', '⛽️', '.']
station = track.index('⛽️')

for _ in range(20):
    print("\n" * 10)
    print(*track)
    time.sleep(1)

    pos = track.index('🚂')
    track[pos] = '.'

    if (pos + 1) % len(track) == station:
        print("The train has stopped on the station")
        time.sleep(3)
        pos = (pos + 2) % len(track)
    else:
        pos = (pos + 1) % len(track)

    track[pos] = '🚂'