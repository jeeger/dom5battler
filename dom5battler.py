#!/usr/bin/python3

import contextlib
import argparse
import os.path
import os

import Map
import Constants


def int_or_quoted_string(string_or_num):
    try:
        return int(string_or_num)
    except ValueError:
        return "\"" + string_or_num + "\""


def read_nonempty(prompt, quit=None, mapper=None):
    # Quit argument is unneeded.
    line = input(prompt)
    while not line:
        print("Please enter something.")
        line = input(prompt)
    if mapper and line != quit:
        return mapper(line)
    return line


def read_repeated(prompt, readfun, quit=None, mapper=None):
    result = []
    line = readfun(prompt, quit=quit, mapper=mapper)
    while line != quit:
        result.append(line)
        line = readfun(prompt, quit=quit, mapper=mapper)
    return result


def read_multiple(prompt, count, mapper=None, quit=None):
    line = read_nonempty(prompt)
    if line == quit:
        return quit
    line = tuple(map(str.strip, line.split(",")))
    while len(line) != count:
        print(f"Enter exactly {count} items.")
        line = read_nonempty(prompt)
        if line == quit:
            return quit
        line = tuple(map(str.strip, line.split(",")))
    if mapper and len(mapper) == count:
        return tuple(map(lambda t: t[1](t[0]) if t[1] else t[0],
                         zip(line, mapper)))
    elif mapper and len(mapper) != count:
        print("Provide a mapper for each field. `None` is identity "
              "function.")
        exit(1)
    return line


def read_units():

    def unit_readfn(p, quit, mapper):
        return read_multiple(p, 2, mapper=mapper, quit=quit)
    return read_repeated("Unit, Quantity: ", unit_readfn,
                         quit=".", mapper=[int_or_quoted_string, int])


def from_file(filename):
    import configparser
    parser = configparser.ConfigParser(allow_no_value=True)
    # Case sensitive option names
    parser.optionxform = str
    parser.read_file(open(filename))
    conf = {}
    conf['testname'] = os.path.splitext(os.path.basename(filename))[0]
    conf['playernation'] = (parser['Nation']['Age'].lower(),
                            parser['Nation']['Name'])
    conf['playercommanders'] = list(map(
        lambda i: int_or_quoted_string(i[0]),
        parser.items('Player Commanders')))
    conf['playerunits'] = list(map(
        lambda i: (int_or_quoted_string(i[0]), int(i[1])),
        parser.items('Player Units')))
    conf['enemycommanders'] = list(map(
        lambda i: int_or_quoted_string(i[0]),
        parser.items('Enemy Commanders')))
    conf['enemyunits'] = list(map(
        lambda i: (int_or_quoted_string(i[0]), int(i[1])),
        parser.items('Enemy Units')))
    return conf


def interactive():
    result = {}
    result['testname'] = read_nonempty("Name for this test: ")

    result['playernation'] = read_multiple(
        "Which nation do you want to play? Enter age (EA, MA, LA) "
        "and name, separated by commas.\nNation: ", 2, [str.lower, None])
    print("Player commander name/number. Exit with '.'")
    result['playercommanders'] = read_repeated(
        "Commander: ", read_nonempty,
        quit=".", mapper=int_or_quoted_string)
    print("Player units. Name/number followed by quantity, separated by "
          "comma. Finish with '.'")
    result['playerunits'] = read_units()
    print("Enemy commanders name/number. Exit with '.'")
    result['enemycommanders'] = read_repeated(
        "Commander: ", read_nonempty,
        quit=".", mapper=int_or_quoted_string)
    print("Enemy units. Name/number followed by quantity, separated by "
          "comma. Finish with '.'")
    result['enemyunits'] = read_units()

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
    print("Your nation: ", conf['playernation'])
    print("Your commanders: ")
    for commander in conf['playercommanders']:
        print(f"\t{commander}")
    print("Your units: ")
    for (unit, quantity) in conf['playerunits']:
        print(f"\t{quantity}x {unit}")
    print("Enemy commanders: ")
    for commander in conf['enemycommanders']:
        print(f"\t{commander}")
    print("Enemy units: ")
    for (unit, quantity) in conf['enemyunits']:
        print(f"\t{quantity}x {unit}")

    if args.domdir:
        map_out = open(os.path.join(args.domdir, "maps",
                                    f"Battle-{conf['testname']}.map"), "w")
    else:
        map_out = open(f"Battle-{conf['testname']}.map", "w")

    with contextlib.redirect_stdout(map_out):
        Map.print_map_header(conf['testname'])
        Map.print_player_setup(conf['playernation'])
        Map.print_units(Constants.land_start_province,
                        conf['playercommanders'],
                        conf['playerunits'], clear=False)
        Map.print_units(Constants.battle_province,
                        conf['enemycommanders'],
                        conf['enemyunits'])
        Map.print_rest()

    if args.mod:
        if args.domdir:
            mod_out = open(os.path.join(args.domdir, "mods",
                                        f"Battle-{conf['testname']}.dm"), "w")
        else:
            mod_out = open(f"Battle-{conf['testname']}.dm", "w")
        with contextlib.redirect_stdout(mod_out):
            Map.print_mod(conf['testname'], conf['playernation'])

    if args.run and args.mod and args.domdir:
        os.system(f"{args.run} --enablemod Battle-{conf['testname']}.dm")
        os.unlink(os.path.join(args.domdir, "mods",
                               f"Battle-{conf['testname']}.dm"))
        os.unlink(os.path.join(args.domdir, "maps",
                               f"Battle-{conf['testname']}.map"))
    elif args.run and not args.mod and not args.domdir:
        print("Generate a mod and specify domdir to use the run feature.")

if __name__ == "__main__":
    main()
