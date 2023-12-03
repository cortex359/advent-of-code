with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

signals: dict = {}
def connect_wires(line):
    a: str
    b: str
    a, b = line.split(" -> ")
    if a.isdigit():
        signals[b] = int(a)
    else:
        x, op, y = a.split(" ")
        if op == "AND" or op == "OR":
            if signals.get(y) is None:
                connect_wires(data[data.e])
                data.append(line)
                continue
            signals[b] = signals[x] & signals[y]
        elif a.count("OR"):
            x, y = a.split(" OR ")
            if signals.get(x) is None or signals.get(y) is None:
                data.append(line)
                continue
            signals[b] = signals[x] | signals[y]
        elif a.count("LSHIFT"):
            x, y = a.split(" LSHIFT ")
            if signals.get(x) is None:
                data.append(line)
                continue
            signals[b] = signals[x] << int(y)
        elif a.count("RSHIFT"):
            x, y = a.split(" RSHIFT ")
            if signals.get(x) is None:
                data.append(line)
                continue
            signals[b] = signals[x] >> int(y)
        elif a.count("NOT"):
            x = a.removeprefix("NOT ")
            if signals.get(x) is None:
                data.append(line)
                continue
            signals[b] = ~signals[x]

for signal in signals:
    if int(signals[signal]) < 0:
        signals[signal] = 65536 + int(signals[signal])
    elif int(signals[signal]) > 65535:
        signals[signal] = int(signals[signal]) - 65536
    print(f"{signal}: {signals[signal]}")
