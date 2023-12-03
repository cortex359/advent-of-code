with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

total_sum = 0
for line in data:
	l, w, h = map(lambda x: int(x), line.split('x'))
	surface = 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)
	total_sum += surface

print(total_sum)

#data=["2x3x4", "1x1x10"]
ribbon_sum = 0
for line in data:
	l, w, h = map(lambda x: int(x), line.split('x'))
	lwh = list(map(lambda x: int(x), line.split('x')))
	lwd = sorted(lwh)
	ribbon = min(2*(l+w), 2*(w+h), 2*(h+l))+ l*w*h
	ribbon_sum += ribbon

print(ribbon_sum)