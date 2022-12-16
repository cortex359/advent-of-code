import time

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]


class Monkey:
	id: int
	items: list[int] = []
	monkey: list[str]
	operation: str

	def __init__(self, id):
		self.id = id
		for l, line in enumerate(data):
			if line == f"Monkey {id}:":
				self.monkey = data[l:l + 6]
				break
		for l in self.monkey:
			if l.strip().startswith("Starting items:"):
				self.items = list(map(int, l.split("items: ")[1].split(",")))
			if l.strip().startswith("Operation"):
				self.operation = l.split(": new = ")[1]
			if l.strip().startswith("Test:"):
				self.div_test = int(l.split("divisible by ")[1])
			if l.strip().startswith("If true:"):
				self.test_ok = int(l.split("monkey ")[1])
			if l.strip().startswith("If false:"):
				self.test_fail = int(l.split("monkey ")[1])
		self.inspected = 0

	def operate(self, worry_lvl):
		self.inspected += 1
		if self.operation.find("+") > 0:
			return worry_lvl + int(self.operation.split(" + ")[1])
		if self.operation.find("*") > 0:
			if self.operation.split(" * ")[0] == self.operation.split(" * ")[1]:
				return worry_lvl * worry_lvl
			else:
				return worry_lvl * int(self.operation.split(" * ")[1])

	def test(self, worry_lvl):
		if worry_lvl % self.div_test == 0:
			return self.test_ok
		else:
			return self.test_fail


def printout(monkeys):
	monkey_business: list[int] = []

	for m in monkeys:
		print(f"Monkey {m.id}, after {m.inspected:6d} inspections: {m.items}")
		monkey_business.append(m.inspected)

	monkey_business.sort()
	print("Monkey Business:\n\t",
			monkey_business[-1], "*", monkey_business[-2], "=", (monkey_business[-1] * monkey_business[-2]))


def start_game(rounds, monkeys, divider=True):
	for r in range(rounds):
		for m in monkeys:
			# print(f"Monkey {m.id}:")
			for i in m.items:
				# print(f"\tMonkey inspects an item with a worry level of {i}.")
				worry_lvl = m.operate(i)
				# print(f"\t\tWorry level is now {worry_lvl}.")
				if divider:
					worry_lvl = worry_lvl // 3
				else:
					# (3 * 11 * 19 * 5 * 2 * 7 * 17 * 13)
					worry_lvl = worry_lvl % 9_699_690
				# print(f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {worry_lvl}.")
				monkeys[m.test(worry_lvl)].items.append(worry_lvl)
			# print(f"\t\tItem with worry level {worry_lvl} is thrown to monkey {m.test(worry_lvl)}.")
			m.items = []


#######################################################################################################################

# Example
# divider = 23 * 19 * 13 * 17
# monkeys = [Monkey(0), Monkey(1), Monkey(2), Monkey(3)]

# Input
# monkeys = [Monkey(0), Monkey(1), Monkey(2), Monkey(3), Monkey(4), Monkey(5), Monkey(6), Monkey(7)]
# divider = 3 * 11 * 19 * 5 * 2 * 7 * 17 * 13

#######################################################################################################################

st = time.time()

# Part I
monkeys = [Monkey(0), Monkey(1), Monkey(2), Monkey(3), Monkey(4), Monkey(5), Monkey(6), Monkey(7)]
start_game(20, monkeys)
printout(monkeys)

et1 = time.time()

# Part II
monkeys = [Monkey(0), Monkey(1), Monkey(2), Monkey(3), Monkey(4), Monkey(5), Monkey(6), Monkey(7)]
start_game(10000, monkeys, divider=False)
printout(monkeys)

et2 = time.time()

print(f"Execution time Part I:  {(et1 - st)  * 1000:10.6f} ms")
print(f"Execution time Part II: {(et2 - et1) * 1000:10.6f} ms")



