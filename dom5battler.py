#!/usr/bin/python3

import contextlib
import argparse
import os.path
import os

import Map
import Constants
import Input


def convert_units(config):
    result = []
    for army in config:
        units = []
        for (name_or_id, count) in army['units'].items():
            units.append(Constants.Unit(name_or_id, count))
        result.append(Constants.Army(
            army['commander'],
            army['items'],
            units))
    return result


def from_file(filename):
    import json
    raw_conf = json.load(open(filename))
    # Case sensitive option names
    conf = {}
    conf['battlename'] = os.path.splitext(os.path.basename(filename))[0]
    conf['player_1_nation'] = Constants.Nation(
        raw_conf['age'], raw_conf['player_1']['nation'])
    conf['player_1_armies'] = convert_units(raw_conf['player_1']['armies'])
    conf['centerarmies'] = convert_units(raw_conf['center'])
    if 'player_2' in raw_conf:
        conf['player_2_nation'] = Constants.Nation(
            raw_conf['age'], raw_conf['player_2']['nation'])
        conf['player_2_armies'] = convert_units(raw_conf['player_2']['armies'])
    return conf


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
        conf = Input.interactive()

    print("Configuration: ")
    print(f"P1 nation: {conf['player_1_nation'].age} {conf['player_1_nation'].name}")
    print("Your armies: ")
    for (armycount, army) in enumerate(conf['player_1_armies']):
        print(f"Army {armycount}:")
        print(f"\tCommander: {army.commander_type}")
        print(f"\tItems: {army.items}")
        print("\tUnits:")
        for unit in army.units:
            print(f"\t\t{unit.count}x {unit.unit_type}")

    if 'centerarmies' in conf:
        print("Center armies: ")
        for (armycount, army) in enumerate(conf['centerarmies']):
            print(f"Army {armycount}:")
            print(f"\tCommander: {army.commander_type}")
            print(f"\tItems: {army.items}")
            print("\tUnits:")
            for unit in army.units:
                print(f"\t\t{unit.count}x {unit.unit_type}")

    if 'player_2_armies' in conf:
        print(f"P2 nation: {conf['player_2_nation'].age} {conf['player_2_nation'].name}")
        print("Your armies: ")
        for (armycount, army) in enumerate(conf['player_1_armies']):
            print(f"Army {armycount}:")
            print(f"\tCommander: {army.commander_type}")
            print(f"\tItems: {army.items}")
            print(f"\tUnits:")
            for unit in army.units:
                print(f"\t\t{unit.count}x {unit.unit_type}")

    if args.domdir:
        map_out = open(os.path.join(args.domdir, "maps",
                                    f"Battle-{conf['battlename']}.map"), "w")
    else:
        map_out = open(f"Battle-{conf['battlename']}.map", "w")

    with contextlib.redirect_stdout(map_out):
        Map.print_map_header(conf['battlename'])
        Map.print_player_setup(conf['player_1_nation'],
                               conf.get('player_2_nation', None))
        Map.print_units(Constants.player_1_start_province,
                        conf.get('player_1_armies'), clear=False)
        Map.print_units(Constants.battle_province,
                        conf.get('centerarmies', []))
        Map.print_units(Constants.player_2_start_province,
                        conf.get('player_2_armies', []), clear=False)
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
