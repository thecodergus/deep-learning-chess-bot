import pickle, numpy as np


if __name__ == "__main__":
    with open("backup.bin", "rb") as f:
        itens = pickle.loads(f.read())

    print(itens)
