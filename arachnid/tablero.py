class Tablero:
    def __init__(self):
        self.columnas = {i : [] for i in range(1,11)} # diccionario con entero como clave y lista como valor. Clave desde 1 a 10
        self.columnas_de_tablero = []
        self.juegos_terminados = []

    def recoger_y_repartir(self, cartas): # salta error si cartas NO es lista o SI NO contiene 44 elementos.
        carta_iterador = iter(cartas)       # reparte a los espacios de cartas, para empezar a jugar.

        for columna in range(1,5): # guarda cartas en las primeras 4 columnas, y 4 filas,
            for _ in range(1,5):
                self.columnas[columna].append(next(carta_iterador))

        for columna in range(5,11): # guarda cartas en las últimas 6 columnas, y 3 filas,
            for _ in range(1,4):
                self.columnas[columna].append(next(carta_iterador))

        for columna in range(1,11):
            carta = next(carta_iterador)
            carta.mostrar()
            carta.bloqueada = False
            carta.carta_encima = False
            self.columnas[columna].append(carta)

    def update_columnas_de_tablero(self):
        for columna in self.columnas.values():
            self.columnas_de_tablero.append(columna)
        return self.columnas_de_tablero # lista con lista de columnas

    def lejos(self, c2): # inicia con el índice de la columna donde tiene que hacer pop
        print("Se comprueba el largo (si es 13 se extrae)")
        print(f"largo : {len(self.columnas_de_tablero[c2][-1])}")
        if len(self.columnas_de_tablero[c2][-1]) == 13:
            print(f"Se tiene que sacar {self.columnas_de_tablero[c2][-1]} del juegoo")
            juego = self.columnas_de_tablero[c2].pop()
            print(f"pero se sacaa: {juego}")
            self.juegos_terminados.append(juego)

        self.fin()

    def fin(self):
        if len(self.juegos_terminados) == 104:
            print(f"GANASTE")
            return