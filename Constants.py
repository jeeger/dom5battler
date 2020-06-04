# regex used to generate this: ^\([0-9]+\)\s-+\([a-zA-Z ’å]+\)\s-+.*
import collections

Army = collections.namedtuple("Army", ["commander_type", "items", "units"])
Unit = collections.namedtuple("Unit", ["unit_type", "count"])
Nation = collections.namedtuple("Nation", ["age", "name"])


gemtypes = {
    "Fire": 0,
    "Air": 1,
    "Water": 2,
    "Earth": 3,
    "Astral": 4,
    "Death": 5,
    "Nature": 6,
    "Blood slave": 7
}

terraintypes = {
    "Plains": 0,
    "Small Province": 1,
    "Large Province": 2,
    "Sea": 4,
    "Freshwater": 8,
    "Highlands": 16,
    "Swamp": 32,
    "Waste": 64,
    "Forest": 128,
    "Farm": 256,
    "Nostart": 512,
    "Many Sites": 1024,
    "Deep Sea": 2048,
    "Cave": 4096,
    "Mountains": 4194304,
    "Good throne location": 16777216,
    "Good start location": 33554432,
    "Bad throne location": 67108864,
    "Warmer": 536870912,
    "Colder": 1073741824,
    "Fire sites": 8192,
    "Air sites": 16384,
    "Water sites": 32768,
    "Earth sites": 65536,
    "Astral sites": 131072,
    "Death sites": 262144,
    "Nature sites": 524288,
    "Blood sites": 1048576,
    "Holy sites": 2097152,
}

nations = {
    "ea": {
        "Arcoscephale": 5,
        "Ermor": 6,
        "Ulm": 7,
        "Marverni": 8,
        "Sauromatia": 9,
        "Tien Chi": 10,
        "Machaka": 11,
        "Mictlan": 12,
        "Abysia": 13,
        "Caelum": 14,
        "Ctis": 15,
        "Pangaea": 16,
        "Agartha": 17,
        "Tir na nOg": 18,
        "Fomoria": 19,
        "Vanheim": 20,
        "Helheim": 21,
        "Niefelheim": 22,
        "Rus": 24,
        "Kailasa": 25,
        "Lanka": 26,
        "Yomi": 27,
        "Hinnom": 28,
        "Ur": 29,
        "Berytos": 30,
        "Xibalba": 31,
        "Mekone": 32,
        "Ubar": 33,
        "Atlantis": 36,
        "Rlyeh": 37,
        "Pelagia": 38,
        "Oceania": 39,
        "Therodos": 40,
    }, "ma": {
        "Arcoscephale": 43,
        "Ermor": 44,
        "Sceleria": 45,
        "Pythium": 46,
        "Man": 47,
        "Eriu": 48,
        "Ulm": 49,
        "Marignon": 50,
        "Mictlan": 51,
        "Tien Chi": 52,
        "Machaka": 53,
        "Agartha": 54,
        "Abysia": 55,
        "Caelum": 56,
        "Ctis": 57,
        "Pangaea": 58,
        "Asphodel": 59,
        "Vanheim": 60,
        "Jotunheim": 61,
        "Vanarus": 62,
        "Bandar Log": 63,
        "Shinuyama": 64,
        "Ashdod": 65,
        "Uruk": 66,
        "Nazca": 67,
        "Xibalba": 68,
        "Phlegra": 69,
        "Phaeacia": 70,
        "Ind": 71,
        "NaBa": 72,
        "Atlantis": 73,
        "Rlyeh": 74,
        "Pelagia": 75,
        "Oceania": 76,
        "Ys": 77,
    }, "la": {
        "Arcoscephale": 80,
        "Pythium": 81,
        "Lemuria": 82,
        "Man": 83,
        "Ulm": 84,
        "Marignon": 85,
        "Mictlan": 86,
        "Tien Chi": 87,
        "Jomon": 89,
        "Agartha": 90,
        "Abysia": 91,
        "Caelum": 92,
        "Ctis": 93,
        "Pangaea": 94,
        "Midgard": 95,
        "Utgard": 96,
        "Bogarus": 97,
        "Patala": 98,
        "Gath": 99,
        "Ragha": 100,
        "Xibalba": 101,
        "Phlegra": 102,
        "Vaettiheim": 103,
        "Atlantis": 106,
        "Rlyeh": 107,
        "Erytheia": 108,
    }
}


def get_different_nation(nation):
    for (othernation, index) in nations[nation.age.lower()].items():
        if othernation != nation.name:
            return index


player_1_start_province = 5
player_2_start_province = 8
battle_province = 10
