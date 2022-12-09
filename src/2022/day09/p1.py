with open("input") as file:
	data = [line.removesuffix("\n") for line in file]


head_x, head_y = 0, 0
seg1_x, seg1_y = 0, 0
seg2_x, seg2_y = 0, 0
seg3_x, seg3_y = 0, 0
seg4_x, seg4_y = 0, 0
seg5_x, seg5_y = 0, 0
seg6_x, seg6_y = 0, 0
seg7_x, seg7_y = 0, 0
seg8_x, seg8_y = 0, 0
tail_x, tail_y = 0, 0

seg1_pos: set([str]) = set()
tail_pos: set([str]) = set()

def tail_follow(hx, hy, tx, ty):
	#print(f"head: {hx}:{hy} tail: {tx}:{ty}")
	if tx == hx:
		if ty == hy or ty == hy - 1 or ty == hy + 1:
			return tx, ty
		elif ty < hy:
			return tx, ty + 1
		elif ty > hy:
			return tx, ty - 1
	if ty == hy:
		if tx == hx or tx == hx - 1 or tx == hx + 1:
			return tx, ty
		elif tx < hx:
			return tx + 1, ty
		elif tx > hx:
			return tx - 1, ty
	# diagonal ajecent
	if ty == hy + 1 and tx == hx + 1:
		return tx, ty
	if ty == hy - 1 and tx == hx - 1:
		return tx, ty
	if ty == hy + 1 and tx == hx - 1:
		return tx, ty
	if ty == hy - 1 and tx == hx + 1:
		return tx, ty
	# diagonal seperate
	# ..T
	# ...
	# .H.
	if ty == hy + 2 and tx == hx + 1:
		return tx-1, ty-1
	# .H.
	# ...
	# ..T
	if ty == hy - 2 and tx == hx + 1:
		return tx-1, ty+1
	# .T.
	# ...
	# ..H
	if ty == hy + 2 and tx == hx - 1:
		return tx+1, ty-1
	# ..H
	# ...
	# .T.
	if ty == hy - 2 and tx == hx - 1:
		return tx+1, ty+1
	# ...
	# ..T
	# H..
	if ty == hy + 1 and tx == hx + 2:
		return tx-1, ty-1
	# H..
	# ..T
	# ...
	if ty == hy - 1 and tx == hx + 2:
		return tx-1, ty+1
	# T..
	# ..H
	# ...
	if ty == hy + 1 and tx == hx - 2:
		return tx+1, ty-1
	# ..H
	# T..
	# ...
	if ty == hy - 1 and tx == hx - 2:
		return tx+1, ty+1

	if ty == hy + 2 and tx == hx + 2:
		return tx-1, ty-1
	if ty == hy - 2 and tx == hx - 2:
		return tx+1, ty+1
	if ty == hy - 2 and tx == hx + 2:
		return tx-1, ty+1
	if ty == hy + 2 and tx == hx - 2:
		return tx+1, ty-1

	print(f"Non if at {hx}:{hy} with tail at {tx}:{ty}")
	return tx, ty


for line in data:
	direction, steps = line.split()
	for s in range(int(steps)):
		if direction == "R":
			head_x += 1
		elif direction == "U":
			head_y += 1
		elif direction == "D":
			head_y -= 1
		elif direction == "L":
			head_x -= 1

		seg1_x, seg1_y = tail_follow(head_x, head_y, seg1_x, seg1_y)
		seg2_x, seg2_y = tail_follow(seg1_x, seg1_y, seg2_x, seg2_y)
		seg3_x, seg3_y = tail_follow(seg2_x, seg2_y, seg3_x, seg3_y)
		seg4_x, seg4_y = tail_follow(seg3_x, seg3_y, seg4_x, seg4_y)
		seg5_x, seg5_y = tail_follow(seg4_x, seg4_y, seg5_x, seg5_y)
		seg6_x, seg6_y = tail_follow(seg5_x, seg5_y, seg6_x, seg6_y)
		seg7_x, seg7_y = tail_follow(seg6_x, seg6_y, seg7_x, seg7_y)
		seg8_x, seg8_y = tail_follow(seg7_x, seg7_y, seg8_x, seg8_y)
		tail_x, tail_y = tail_follow(seg8_x, seg8_y, tail_x, tail_y)

		seg1_pos.add(str(seg1_x) + ":" + str(seg1_y))
		tail_pos.add(str(tail_x) + ":" + str(tail_y))

	print(f"== {line} ==")
	print(f"->\thead: {head_x}:{head_y}, seg1: {seg1_x}:{seg1_y}, tail: {tail_x}:{tail_y}")

print(f"positions visited by rope 1st segment: {len(seg1_pos)}")
print(f"positions visited by rope tail: {len(tail_pos)}")
