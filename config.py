# Constantes do Bingo
MIN_NUMBER = 1
MAX_NUMBER = 75
BINGO_COLUMNS = {
    'B': (1, 15),
    'I': (16, 30),
    'N': (31, 45),
    'G': (46, 60),
    'O': (61, 75)
}

def get_initial_numbers():
    return list(range(MIN_NUMBER, MAX_NUMBER + 1))
