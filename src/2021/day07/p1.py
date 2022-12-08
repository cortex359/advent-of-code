import numpy as np
import statistics

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

#data[0] = "16,1,2,0,4,2,7,1,2,14"

pos: list[int] = list(map(int, data[0].split(",")))
mean: int = int(statistics.median(pos))
fuel = 0
for p in pos:
	fuel += abs(p - mean)

print("Results:")
print(f"Fuel calculation 1: {fuel:,}")

fuel_consumptions: list[int] = []
avge: int = round(statistics.mean(pos))
for a in range(avge-20, avge+20):
	fuel = 0
	for p in pos:
		for i in range(1, abs(p - a)+1):
			fuel += i
	fuel_consumptions.append(fuel)
	# print(f"{a:4d}: {fuel}")

fuel_consumptions.sort()

print(f"Fuel calculation 2: {fuel_consumptions[0]:,}")