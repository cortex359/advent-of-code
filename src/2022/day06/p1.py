with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

signal = data[0]

example_results = [
	-1, 5, 6, 10, 11,
	19, 23, 23, 29, 26
]
example_data = [
	"mjqjpqmgbljsphdztnvjfqwrcgsmlb",
	"bvwbjplbgvbhsrlpgdmjqwftvncz",
	"nppdvjthqldpwncqszvftbrmjlhg",
	"nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
	"zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
]

def get_start_of_packet_marker(signal, marker_length):
	for v in range(len(signal)):
		package = signal[v:v+marker_length]
		package_set = set(package)
		if len(package_set) == len(package):
			return v+marker_length

print("→ Testing examples:")
for n, example in enumerate(example_data):
	if example_results[n] != -1:
		print(f"Start of size  4 packet marker: {get_start_of_packet_marker(example,  4):2d}, expected: {example_results[n]:2d}")
	print(f"Start of size 14 packet marker: {get_start_of_packet_marker(example, 14):2d}, expected: {example_results[n+5]:2d}")

print("\n→ Testing input file:")
print(f"Start of size  4 packet marker: {get_start_of_packet_marker(signal,  4):4d}")
print(f"Start of size 14 packet marker: {get_start_of_packet_marker(signal, 14):4d}")