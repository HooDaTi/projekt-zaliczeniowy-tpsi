numbers = [int(x) for x in input("Podaj liczby oddzielone spacją: ").split()]
even_numbers = [n for n in numbers if n % 2 == 0]
print("Liczby parzyste:", even_numbers)