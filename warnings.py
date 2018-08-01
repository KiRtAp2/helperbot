import json

warnings = {}

with open("warnings.json", "r") as f:
    warnings = json.load(f)


def write():
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, ensure_ascii=False)

def warn(user: str,
         write_to_file=True):
    global warnings
    if user in warnings:
        warnings[user] += 1
    else:
        warnings[user] = 1

    if write_to_file:
        write()

def get_warnings(user):
    if user in warnings:
        return warnings[user]
    else:
        return 0