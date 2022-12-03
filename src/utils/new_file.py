import os
import sys
import requests

def get_session_id(filename):
    with open(filename) as f:
        return f.read().strip()


def get_url(year, day):
    return f"https://adventofcode.com/{year}/day/{day}/input"


def save_input(day, year=2022):
    directory = f"src/{year:04d}/day{day:02d}"
    filename = "input"

    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        url = get_url(year, day)
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if not response.ok:
            raise RuntimeError(
                f"Request failed\n\tstatus code: {response.status_code}\n\tmessage: {response.content}"
            )
        with open(path, "w") as file:
            file.write(response.text[:-1])


SESSION_ID_FILE = "session.cookie"
HEADERS = {
    "User-Agent": "cortex359 python script"
}
COOKIES = {
    "session": get_session_id(SESSION_ID_FILE)
}

day = int(sys.argv[1])
if len(sys.argv) > 2:
    year = int(sys.argv[2])
else:
    year = 2022

DEFAULT_FILE = f"with open(\"input\") as file:\n\tdata = [line.removesuffix(\"\\n\") for line in file]\n\nfor line in data:\n\t\n"

directory = ""
filename = "p1.py"

for d in ["src", f"{year:04d}", f"day{day:02d}"]:
    directory = os.path.join(directory, d)
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError as error:
            print(error)

print("Saving input:")
save_input(day, year)

path = os.path.join(directory, filename)
if os.path.exists(path):
    print("Python file exisits.")
else:
    with open(path, "x") as file:
        file.write(DEFAULT_FILE)

print(f"Happy coding: {path}")
