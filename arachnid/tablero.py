from openpyxl.xml import defusedxml_env_set


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
        if len(self.columnas_de_tablero[c2][-1]) == 13:
            juego = self.columnas_de_tablero[c2].pop()
            self.juegos_terminados.append(juego)
            try:
                self.columnas_de_tablero[c2][-1].mostrar()
            except (AttributeError, IndexError):
                pass
        self.fin()

    def fin(self):
        print("juegos terminados: ",len(self.juegos_terminados))
        if len(self.juegos_terminados) == 8:
            print()
            print(f"GANASTE")
            print()
            return

    def prepare_list(self,c1,i):
        lista1 = self.columnas_de_tablero[c1][-1][i:]
        self.columnas_de_tablero[c1][-1]= self.columnas_de_tablero[c1][-1][:i]
        self.columnas_de_tablero[c1][-1].append(lista1)

    def move_to_empty_col(self, col1, col2): # mueve sin reglas, el último elemento de la columma c1 a el último lugar de la columna c2
        elemento = self.columnas_de_tablero[col1].pop()
        self.columnas_de_tablero[col2].append(elemento)

    def move_card_to_card(self, col1, col2, mismo_palo=True):# usar solamente cuando el último elemento de las columnas es una carta SOLA
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
            carta1 = col1.pop()
            self.columnas_de_tablero[col2].append(carta1)

    def move_list_to_list(self, col1, col2, mismo_palo=True):
        if mismo_palo:
            lista1 = self.columnas_de_tablero[col1].pop()
            self.columnas_de_tablero[col2][-1].extend(lista1)
        else:
            lista1 = col1.pop()
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

    def fix_col(self,col1, col2):
        self.lejos(col2)
        if len(self.columnas_de_tablero[col1]) > 0:
            if isinstance(self.columnas_de_tablero[col1][-1], list):
                if len(self.columnas_de_tablero[col1][-1]) == 0:
                    print("Lista vacía se elimina correctamente, FUNCIONÉ :DDDDDD")
                    self.columnas_de_tablero[col1] = col1.pop()
                    print("Tengo que mostrar c1? D:")
                elif len(self.columnas_de_tablero[col1][-1]) == 1:
                    print("FUAAA arreglo c1 :D")
                    print(f"antes: {self.columnas_de_tablero[col1]}")
                    self.columnas_de_tablero[col1][-1] = self.columnas_de_tablero[col1][-1][0]
                    print(f"después: {self.columnas_de_tablero[col1]}")
            else:
                try:
                    print("Apuntamos a la carta y la mostramos si no está mostrada:")
                    print(f"columna antes del intento: {self.columnas_de_tablero[col1]}")
                    self.columnas_de_tablero[col1][-1].mostrar()
                    print(f"Columna después: {self.columnas_de_tablero[col1]}")
                except Exception as e:
                    print("Manejar exception ::::: ",e)
        print()
        print("Me faltó algo? fin del fix :p ¿fixed?")


