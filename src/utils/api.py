import requests
import os


def get_session_id(filename):
    with open(filename) as f:
        return f.read().strip()


def get_url(year, day):
    return f"https://adventofcode.com/{year}/day/{day}/input"


SESSION_ID_FILE = "session.cookie"
HEADERS = {
    "User-Agent": "cortex359 python script"
}
COOKIES = {
    "session": get_session_id(SESSION_ID_FILE)
}


def get_input(day, year=2022):
    directory = "inputs"
    filename = f"{year:4d}_{day:02d}.0"
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError as error:
            print(error)

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

    with open(path) as file:
        return [line.removesuffix("\n") for line in file]
