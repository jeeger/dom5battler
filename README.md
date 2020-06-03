# Dom5Battler

Quick and dirty Python script to set up battles for testing in Dominions.

## Requirements

Python 3. The [Arena map](https://steamcommunity.com/sharedfiles/filedetails/?id=1404827698) should
be installed in Dominions, as the script reuses assets from the Arena map.

## Usage

The script can be used both interactively and noninteractively, with a configuration file.

To run interactively, just run "./dom5battler.py". The script will then query you for a name, your
nation and age, your commanders and units and enemy commanders and units. Enemy units will be put
into province 10, the center province.

To run noninteractively, run ```./dom5battler.py -f example.conf```. This will read the example
file and create a map for you.

After running, you will have a ```<name>.map``` file. Copy this to your Dominions map folder, and
create a new game, selecting the map. There will be exactly two nations available, select the one
you chose in the setup, create a pretender and click through. The arena map will be set up with the
units you have chosen. Attack with your units, and view the results of the battle at the end of the
turn.

Units and commanders can be specified via name or numbers.

## Other features

This script has some extra functionality to make setting up battles even easier: When given the
```-m``` argument, it will include a modified copy of the [Debug
mod](https://illwiki.com/dom5/debug-mod), and create an event that will give you some gems and a
Debug sensei in your first turn. This means you don't even need to design a special pretender,
simply click through, and you will be able to do everything with the Debug Sensei.

When passed ```-r <dom5binary>```, the script will automatically run Dominions 5 with the correct
mod loaded, and delete the map and mod files afterwards (be careful about not reusing a name of an
existing mod or map, as this will overwrite and subsequently delete the mod or map). You will also
need to specify ```-d <userdir>``` so the script knows where to put the generated files.

## TBD

Items and Terrain is currently still TBD.
