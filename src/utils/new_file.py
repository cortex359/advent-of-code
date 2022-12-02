import os
print(os.listdir("."))
l = filter(lambda x: "__" not in x and "day" in x, os.listdir("src"))
l = list(l)
n = int(sorted(l)[-1][3:5])+1 if len(l) > 0 else 1


DEFAULT_FILE = f"from utils.api import get_input\n\ninput_str = get_input({n})\n\n# WRITE YOUR SOLUTION HERE\n\n"


path = f"src/day{n:02d}.py"

with open(path, "w") as f:
    f.write(DEFAULT_FILE)

print(f"Enter your solution in {path}")
