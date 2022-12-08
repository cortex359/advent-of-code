with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

fish: list[str] = data[0].split(",")

fish_timers: dict = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}

for t in fish:
	fish_timers[t] += 1

for day in range(1, 257):
	new = fish_timers["0"]
	fish_timers["0"] = fish_timers["1"]
	fish_timers["1"] = fish_timers["2"]
	fish_timers["2"] = fish_timers["3"]
	fish_timers["3"] = fish_timers["4"]
	fish_timers["4"] = fish_timers["5"]
	fish_timers["5"] = fish_timers["6"]
	fish_timers["6"] = fish_timers["7"]
	fish_timers["7"] = fish_timers["8"]

	fish_timers["6"] += new
	fish_timers["8"] = new

	fish_total = sum(fish_timers.values())
	print(f"Day {day:2d}: [{fish_total:5d}]")

	
