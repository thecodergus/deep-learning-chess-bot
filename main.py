import chess, glob, tqdm, numpy as np, pickle
import chess.pgn
from dataclasses import dataclass
import psycopg2
import chess.engine

# from tensorflow import keras

# Costantes
ENGINE = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-ubuntu-x86-64")
FEN_MAX = 73
# Definir as letras correspondentes na tabela ASCII
letras = {
    "r": 1,  # ord("r"),
    "n": 2,  # ord("n"),
    "b": 3,  # ord("b"),
    "q": 4,  # ord("q"),
    "k": 5,  # ord("k"),
    "p": 6,  # ord("p"),
    "R": 7,  # ord("R"),
    "N": 8,  # ord("N"),
    "B": 9,  # ord("B"),
    "Q": 10,  # ord("Q"),
    "K": 11,  # ord("K"),
    "P": 12,  # ord("P"),
    ".": 0,
}
casas = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}


def fen_to_numpy_flat(fen):
    # Inicializar um array NumPy 64 elementos com zeros
    tabuleiro = np.zeros(64, dtype=np.float32)

    # Dividir a notação FEN em suas partes
    partes = fen.split()

    # Converter a descrição do tabuleiro para um array unidimensional NumPy
    index = 0
    for char in partes[0]:
        if char == "/":
            continue  # Ignorar a barra "/"
        elif char.isdigit():
            index += int(char)  # Avançar para o próximo índice com base no número
        else:
            tabuleiro[index] = letras[char]
            index += 1

    # Normalizar os valores para o intervalo [0, 1]
    tabuleiro /= max(tabuleiro)

    return tabuleiro


def evaluate_position(fen, turn):
    info = ENGINE.analyse(chess.Board(fen), chess.engine.Limit(time=0.1))

    score = info["score"].relative.score()

    return score


def analyze_game(game):
    board = chess.Board()
    rows = []

    for move in game.mainline_moves():
        color = board.turn
        fen = board.fen()
        binary = board.board_fen()

        try:
            evaluation = evaluate_position(
                fen, board.turn
            )  # Você pode adicionar a lógica para avaliação aqui
            row = (color == chess.WHITE, binary, str(move), float(evaluation))
        except:
            continue
        board.push(move)
        rows.append(row)

    return rows


def process_pgn(file_path) -> list[str]:
    with open(file_path) as f:
        game = chess.pgn.read_game(f)
        rows = analyze_game(game)

    return rows


if __name__ == "__main__":
    result = [process_pgn(i) for i in tqdm.tqdm(glob.glob("download/*.pgn"))]

    with open("backup.bin", "wb") as f:
        f.write(pickle.dumps(result))

    # x = []
    # y_1, y_2 = [], []
    # for caso in tqdm(glob.glob("download/*.pgn")):
    #     for item in process_pgn(caso):
    #         cor, tabuleiro_atual, proximo_movimento, score = item

    #         # 1 se for preto e 0 se for branco
    #         cor = 0 if cor == chess.WHITE else 1

    #         x.append(np.append(fen_to_numpy_flat(tabuleiro_atual), np.float32(cor)))

    #         saida = proximo_movimento[:2]
    #         destino = proximo_movimento[2:]

    #         y_1.append([casas[saida[0]], int(saida[1])])
    #         y_2.append([casas[destino[0]], int(destino[1])])

    # x = np.array(x, dtype=np.float32)
    # y_1 = np.array(y_1, dtype=np.float32)
    # y_2 = np.array(y_2, dtype=np.float32)

    # print(f"x: {x.shape}")
    # print(f"y_1: {y_1.shape}")
    # print(f"y_2: {y_2.shape}")
