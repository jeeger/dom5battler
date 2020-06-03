# regex used to generate this: ^\([0-9]+\)\s-+\([a-zA-Z ’å]+\)\s-+.*

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
    age = nation[0]
    name = nation[1]
    for (nation, index) in nations[age].items():
        if nation != name:
            return (age, nation)


land_start_province = 5
ai_land_start_province = 8
battle_province = 10
