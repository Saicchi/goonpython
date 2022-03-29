"""
Decode latex gloves fingerprints for Goon Security
"""

ALLOWED_CHARACTERS = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z"
]


def match_id(prints: list) -> str:
    characters = prints[0]
    if len(prints) == 1:
        return False

    for charlist in prints[1:]:
        for index, character in enumerate(charlist):
            id_char = characters[index]

            if character not in ALLOWED_CHARACTERS:
                continue

            if id_char not in ALLOWED_CHARACTERS:
                characters[index] = character
                continue

            if character != id_char:
                raise Exception(
                    f"Valid characters are different. Index {index}, {character} != {id_char}")

    for character in characters:
        if character not in ALLOWED_CHARACTERS:
            return False

    return ''.join(characters)


while True:
    ids_list = []
    while True:
        all_allowed = True
        id_input = input("ID: ")

        if id_input in ("r", "R", "reset"):
            print("Resetting")
            ids_list = []
            break

        if len(id_input) != 32:
            print(f"Length does not match. Needs 32, has {len(id_input)}")
            continue

        for character in id_input:
            if character not in ALLOWED_CHARACTERS:
                all_allowed = False
                ids_list.append(list(id_input))
                break

        if all_allowed:
            print(f"\n{id_input}")
            ids_list = []
            print("Resetting\n")
            continue

        filled_id = match_id(ids_list)
        if filled_id:
            print(f"\n{filled_id}")
            ids_list = []
            print("Resetting\n")
            continue
