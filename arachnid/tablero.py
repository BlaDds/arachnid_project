class Tablero:
    def __init__(self):
        self.columnas = {i : [] for i in range(1,11)}
        self.columnas_de_tablero = []
        self.juegos_terminados = []

    def recoger_y_repartir(self, cartas): # reparte solo al principio, las cartas que se ven al empezar el juego.
        carta_iterador = iter(cartas)

        for columna in range(1,5): # guarda cartas en las primeras 4 columnas, y 4 filas.
            for _ in range(1,5):
                self.columnas[columna].append(next(carta_iterador))

        for columna in range(5,11): # guarda cartas en las últimas 6 columnas, y 3 filas.
            for _ in range(1,4):
                self.columnas[columna].append(next(carta_iterador))

        for columna in range(1,11): # reparte las últimas cartas que se ven al principio del juego.
            carta = next(carta_iterador)
            carta.mostrar()
            carta.bloqueada = False
            self.columnas[columna].append(carta)

    def update_columnas_de_tablero(self):
        for columna in self.columnas.values():
            self.columnas_de_tablero.append(columna)
        return self.columnas_de_tablero # lista con lista de columnas

    def move_away(self, c2): # Observa las listas de cartas de un mismo palo,
        # Para eliminar las listas completadas. (Desde A hasta K)
        if len(self.columnas_de_tablero[c2][-1]) == 13:
            juego = self.columnas_de_tablero[c2].pop()
            self.juegos_terminados.append(juego)
            try:
                self.columnas_de_tablero[c2][-1].mostrar()
            except (AttributeError, IndexError):
                pass

    def prepare_list(self,c1,indice_carta): # prepara una lista para mover a c2.
        try:
            lista1 = self.columnas_de_tablero[c1][-1][indice_carta:]
            self.columnas_de_tablero[c1][-1] = self.columnas_de_tablero[c1][-1][:indice_carta]
            self.columnas_de_tablero[c1].append(lista1)
        except (TypeError, AttributeError, IndexError):
            pass


    def move_to_empty_col(self, col1, col2): # mueve sin reglas, el último elemento de la columma c1 a el último lugar de la columna c2
        elemento = self.columnas_de_tablero[col1].pop()
        self.columnas_de_tablero[col2].append(elemento)

    def move_card_to_card(self, col1, col2, mismo_palo=True):# usar solamente cuando el último elemento de las columnas es una carta
        if mismo_palo:
            carta1 = self.columnas_de_tablero[col1].pop()
            carta2 = self.columnas_de_tablero[col2].pop()
            self.columnas_de_tablero[col2].append([carta2,carta1])
        else:
            carta1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2].append(carta1)

    def move_card_to_list(self, col1, col2, mismo_palo=True):
        if mismo_palo:
            carta1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2][-1].append(carta1)
        else:
            carta1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2].append(carta1)

    def move_list_to_list(self, col1, col2, mismo_palo=True):
        if mismo_palo:
            lista1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2][-1].extend(lista1)
        else:
            lista1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2].append(lista1)

    def move_list_to_card(self, col1, col2, mismo_palo=True):
        if mismo_palo:
            lista1 = self.columnas_de_tablero[col1].pop()
            carta2 = self.columnas_de_tablero[col2].pop()
            lista1.insert(0,carta2)
            self.columnas_de_tablero[col2].append(lista1)
        else:
            lista1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2].append(lista1)

    def fix_col(self,col1, col2): # Revisa las columnas para que no queden cartas sin mostrar o listas vacías
        try:
            self.move_away(col2)
        except (TypeError, AttributeError):
            pass

        if len(self.columnas_de_tablero[col2]) > 0:
            if isinstance(self.columnas_de_tablero[col2][-1],list):
                if len(self.columnas_de_tablero[col2][-1]) == 1:
                    self.columnas_de_tablero[col2][-1] = self.columnas_de_tablero[col2][-1][0]
                elif len(self.columnas_de_tablero[col2][-1]) == 0:
                    self.columnas_de_tablero[col2].pop()
        if len(self.columnas_de_tablero[col1]) > 0:
            if isinstance(self.columnas_de_tablero[col1][-1], list):
                if len(self.columnas_de_tablero[col1][-1]) == 0:
                    self.columnas_de_tablero[col1] = self.columnas_de_tablero[col1].pop()
                elif len(self.columnas_de_tablero[col1][-1]) == 1:
                    self.columnas_de_tablero[col1][-1] = self.columnas_de_tablero[col1][-1][0]

        try:
            self.columnas_de_tablero[col1][-1].mostrar()
        except (TypeError, AttributeError, IndexError):
            pass
        try:
            self.columnas_de_tablero[col2][-1].mostrar()
        except (TypeError,AttributeError, IndexError):
            pass
        print()





