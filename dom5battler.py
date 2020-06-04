#!/usr/bin/python3

import contextlib
import argparse
import os.path
import os
import collections

import Map
import Constants


Army = collections.namedtuple("Army", ["commander_type", "items", "units"])
Unit = collections.namedtuple("Unit", ["unit_type", "count"])
Nation = collections.namedtuple("Nation", ["age", "name"])


class QuitEntryException(Exception):
    pass


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
                          quit=quit, mapper=lambda x: Unit(*x))
    return Army(commander_type, items, units)


def convert_units(config):
    result = []
    for army in config:
        units = []
        for (name_or_id, count) in army['units'].items():
            units.append(Unit(name_or_id, count))
        result.append(Army(
            army['type'],
            army['items'],
            units))
    return result


def from_file(filename):
    import json
    raw_conf = json.load(open(filename))
    # Case sensitive option names
    conf = {}
    conf['battlename'] = os.path.splitext(os.path.basename(filename))[0]
    conf['nation'] = Nation(raw_conf['age'], raw_conf['nation'])
    conf['playerarmies'] = convert_units(raw_conf['player'])
    conf['enemyarmies'] = convert_units(raw_conf['enemy'])
    return conf


def interactive():
    result = {}
    result['battlename'] = read_nonempty("Name for this battle: ")
    result['nation'] = Nation(*read_multiple(
        "Which nation do you want to play? Enter age (EA, MA, LA) "
        "and name, separated by commas.\nNation: ", 2))
    print("Construct your armies.\n"
          "Enter commander name or ID, then enter all items this "
          "commander should have, separated by commas.\n"
          "Finally, enter unit name and quantity separated by comma.\n"
          "Finish by entering a bare dot.")
    result['playerarmies'] = read_repeated("== Army ==\n",
                                           lambda: read_army(""))
    print("Construct enemy armies the same way.\n")
    result['enemyarmies'] = read_repeated("== Army ==\n",
                                          lambda: read_army(""))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domdir', '-d', help="Dominions directory. If set, "
                        "write map and mod there, otherwise write into the "
                        "working directory.",
                        default="")
    parser.add_argument('--mod', '-m', help="Also generate event mod.",
                        action='store_true')
    parser.add_argument('--run', '-r', help="Run Dominions with the newly "
                        "generated mod. Removes map and mod after quitting"
                        " Dominions. Argument is the dom5 binary name.",
                        default="")
    parser.add_argument('--file', '-f', help="Configuration file. If not"
                        "provided, run interactively. Some features can "
                        "only be used with the config file.",
                        default="")
    args = parser.parse_args()

    conf = {}
    if args.file:
        conf = from_file(args.file)
    else:
        conf = interactive()

    print("Configuration: ")
    print(f"Your nation: {conf['nation'].age} {conf['nation'].name}")
    print("Your armies: ")
    for (armycount, army) in enumerate(conf['playerarmies']):
        print(f"Army {armycount}:")
        print(f"\tCommander: {army.commander_type}")
        print(f"\tItems: {army.items}")
        for unit in army.units:
            print(f"\t\t{unit.count}x {unit.unit_type}")

    print("Enemy armies: ")
    for (armycount, army) in enumerate(conf['enemyarmies']):
        print(f"Army {armycount}:")
        print(f"\tCommander: {army.commander_type}")
        print(f"\tItems: {army.items}")
        print("\tUnits:")
        for unit in army.units:
            print(f"\t\t{unit.count}x {unit.unit_type}")

    if args.domdir:
        map_out = open(os.path.join(args.domdir, "maps",
                                    f"Battle-{conf['battlename']}.map"), "w")
    else:
        map_out = open(f"Battle-{conf['battlename']}.map", "w")

    with contextlib.redirect_stdout(map_out):
        Map.print_map_header(conf['battlename'])
        Map.print_player_setup(conf['nation'])
        Map.print_units(Constants.land_start_province,
                        conf['playerarmies'], clear=False)
        Map.print_units(Constants.battle_province,
                        conf['enemyarmies'])
        Map.print_rest()

    if args.mod:
        if args.domdir:
            mod_out = open(os.path.join(args.domdir, "mods",
                                        f"Battle-{conf['battlename']}.dm"), "w")
        else:
            mod_out = open(f"Battle-{conf['battlename']}.dm", "w")
        with contextlib.redirect_stdout(mod_out):
            Map.print_mod(conf['battlename'], conf['playernation'])

    if args.run and args.domdir:
        if args.mod:
            os.system(f"{args.run} --enablemod Battle-{conf['battlename']}.dm")
        else:
            os.system(f"{args.run}")
        if args.mod:
            os.unlink(os.path.join(args.domdir, "mods",
                                   f"Battle-{conf['battlename']}.dm"))
        os.unlink(os.path.join(args.domdir, "maps",
                               f"Battle-{conf['battlename']}.map"))
    elif args.run and not args.domdir:
        print("Generate a mod and specify domdir to use the run feature.")


if __name__ == "__main__":
    main()
