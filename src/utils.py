# Common functions used by the other files

def load_fragments() -> list:
    # Load the fragments informations
    fragments_coordinates = []
    with open('../fragments.txt') as f:
        lines = f.read().split('\n')

        for line in lines:
            info = line.split(' ')
            # Info = [2, 575, 640, -54.0116]
            if len(info) == 4:
                fragments_coordinates.append({
                    "num":      int(info[0]),
                    "x":        int(info[1]),
                    "y":        int(info[2]),
                    "rotation": float(info[3]),
                    "image_name": "frag_eroded_" + str(info[0]) + ".png"
                })

    return fragments_coordinates


def load_wrong_fragments_numbers() -> list(int):
    # Load the wrong fragments numbers
    wrong_fragments_numbers = []
    with open('../fragments_s.txt') as f:
        lines = f.read().split('\n')

        for line in lines:
            if len(line) > 0:
                wrong_fragments_numbers.append(int(line))

    return wrong_fragments_numbers
