from itertools import combinations

with open("zoo.txt", "r") as f:
    zoo = f.read().split("\n")

text = input("Letter Box: ").lower()
num = int(input("#Words[num]: "))

for animal in zoo:
    if not all([c in text for c in animal]):
        zoo.remove(animal)


for animals in combinations(zoo, num):
    chimera = "".join(animals)
    if len(chimera) != len(text):
        continue
    if "".join(sorted(chimera)) == "".join(sorted(text)):
        print(f"{animals=}")
        break
