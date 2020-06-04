import Constants


class QuitEntryException(Exception):
    pass


def read_oneof(prompt, possible, quit=None, mapper=None):
    line = input(prompt)
    if line == quit:
        raise QuitEntryException
    while line not in possible:
        print(f"Please enter one of the choices from {possible}.")
        line = input(prompt)
        if line == quit:
            raise QuitEntryException
    return mapper(line)


def read_nonempty(prompt, allow_empty=False, quit=None, mapper=None):
    line = input(prompt)
    while not line and not allow_empty:
        print("Please enter something.")
        line = input(prompt)
    if line == quit:
        raise QuitEntryException
    if mapper:
        return mapper(line)
    return line


def read_repeated(prompt, readfun, quit=None, mapper=None):
    result = []
    try:
        while True:
            line = readfun()
            if mapper:
                result.append(mapper(line))
            else:
                result.append(line)
    except QuitEntryException:
        return result


def read_multiple(prompt, count, mapper=None, quit=None):
    line = read_nonempty(prompt, quit=quit)
    line = tuple(map(str.strip, line.split(",")))
    while len(line) != count:
        print(f"Enter exactly {count} items.")
        line = read_nonempty(prompt, quit=quit)
        line = tuple(map(str.strip, line.split(",")))
    if mapper and len(mapper) == count:
        return tuple(map(lambda t: t[1](t[0]) if t[1] else t[0],
                         zip(line, mapper)))
    elif mapper and len(mapper) != count:
        print("Provide a mapper for each field. `None` is identity "
              "function.")
        exit(1)
    return line


def read_list(prompt, mapper=None, quit=None):
    try:
        line = read_nonempty(prompt, quit=quit, allow_empty=True)
    except QuitEntryException:
        return []
    if not line:
        return []
    if mapper:
        return list(map(lambda e: mapper(str.strip(e)), line.split(",")))
    return list(map(str.strip, line.split(",")))


def make_multiple_reader(prompt, count, mapper, quit):
    def readerfn():
        return read_multiple(prompt, count, mapper=mapper, quit=quit)
    return readerfn


def read_army(prompt, mapper=None, quit="."):
    commander_type = read_nonempty("Commander name/ID: ", quit=quit)
    items = read_list("Items: ", quit=quit)
    units = read_repeated("Units\n",
                          make_multiple_reader(
                              "Unit name/ID, quantity: ", 2,
                              [None, int], quit=quit),
                          quit=quit, mapper=lambda x: Constants.Unit(*x))
    return Constants.Army(commander_type, items, units)


def interactive():
    result = {}
    result['battlename'] = read_nonempty("Name for this battle: ")
    result['player_1_nation'] = Constants.Nation(*read_multiple(
        "Which nation for player 1? Enter age (EA, MA, LA) "
        "and name, separated by commas.\nNation: ", 2))
    print("Construct your armies.\n"
          "Enter commander name or ID, then enter all items this "
          "commander should have, separated by commas.\n"
          "Finally, enter unit name and quantity separated by comma.\n"
          "Finish by entering a bare dot.")
    result['player_1_armies'] = read_repeated("", lambda: read_army(""))
    print("Do you want a center army?")
    if read_oneof("(Y/N): ", set("YNyn"),
                  mapper=lambda c: c.upper() == "Y"):
        print("Construct center armies the same way.\n")
        result['centerarmies'] = read_repeated(
            "", lambda: read_army(""))
    print("Do you want a second human player?")
    if read_oneof("(Y/N): ", set("YNyn"),
                  mapper=lambda c: c.upper() == "Y"):
        result['player_2_nation'] = Constants.Nation(*read_multiple(
            "Which nation for player 2? Enter age (EA, MA, LA) "
            "and name, separated by commas.\nNation: ", 2))
        if result['player_2_nation'].age != result['player_1_nation'].age:
            print("You must select two nations in the same age.")
            exit(1)
        result['player2_armies'] = read_repeated("", lambda: read_army(""))
    return result
