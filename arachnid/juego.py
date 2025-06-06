import random
from .carta import Carta
from .mazo_de_reparto import MazoDeReparto
from .tablero import Tablero


class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.mazo_de_reparto = MazoDeReparto()
        self.baraja_de_inicio = []
        self.fin = False

    def user_won(self):
        if self.fin:
            print("HAS GANADOOO")
            return
    def crear_cartas(self): # creates
        for cantidad in range(8): # Crea 8 juegos completos de cartas. (Juego de carta: desde A hasta K)
            for _ in range(1,14): # Valores de carta, desde 1 a 13
                if cantidad % 2 == 0:# Crea 4 juegos completos de ambos palos.
                    self.baraja_de_inicio.append(Carta(valor=_, palo="♥")) # El palo se puede cambiar a gusto. Predeterminado = "♥"
                else:
                    self.baraja_de_inicio.append(Carta(valor=_, palo="♦")) # El palo se puede cambiar a gusto. Predeterminado = "♦"

    def mezclar(self):
        random.shuffle(self.baraja_de_inicio)

    def repartir_a_tablero(self): # Las 44 cartas que estarán presentes (visibles "A♦" y no visibles "█")
        cartas_separadas = [self.baraja_de_inicio.pop() for _ in range(44)]
        self.tablero.recoger_y_repartir(cartas=cartas_separadas)

    def repartir_a_mazo(self): # las 60 cartas restantes para repartir cuando se quiera
        self.mazo_de_reparto.guardar_cartas_a_repartir(cartas=self.baraja_de_inicio)

    def repartos_restantes_en_mazo(self): # Muestra número de repartos restantes
        return self.mazo_de_reparto.repartos_restantes

    def repartir(self): # Reparte una por una las cartas a la última posición de cada columna
        estas = self.mazo_de_reparto.repartiendo()
        if isinstance(estas, list):
            self.actualizar(estas)
        else:
            return

    def actualizar(self, cartas): # Muestra las últimas cartas repartidas.
        for index, lista in enumerate(self.tablero.columnas_de_tablero):
            try:
                if isinstance(self.tablero.columnas_de_tablero[index][-1], list):
                    carta = self.tablero.columnas_de_tablero[index][-1][-1]
                    if carta.palo == cartas[index].palo and carta.valor == cartas[index].valor+1:
                        self.tablero.columnas_de_tablero[index][-1].append(cartas[index])
                        self.tablero.lejos(index)
                    else:
                        self.tablero.columnas_de_tablero[index].append(cartas[index])
                else:
                    carta = self.tablero.columnas_de_tablero[index][-1]
                    if carta.palo == cartas[index].palo and carta.valor == cartas[index].valor + 1:
                        carta = self.tablero.columnas_de_tablero[index].pop()
                        self.tablero.columnas_de_tablero[index].append([carta,cartas[index]])
                        self.tablero.lejos(index)
                    else:
                        self.tablero.columnas_de_tablero[index].append(cartas[index])
            except IndexError:
                self.tablero.columnas_de_tablero[index].append(cartas[index])

    def analizar(self, c1, c2): # Analiza jugadas adecuadas e incorrectas
        if not isinstance(c1,int):
            print("Ingresa un valor para la primer columna")
            return
        elif not isinstance(c2,int):
            print("ingresa un valor para la segunda columna")
            return

        carta2 = 0
        lista_carta2 = []
        if len(self.tablero.columnas_de_tablero[c1]) == 0: # c1 es la columna vacía
            print("Elige una columna con cartas")
            return
        if len(self.tablero.columnas_de_tablero[c2]) == 0: # c2 está vacío, nada para analizar, se mueve c1 a c2
            if len(self.tablero.columnas_de_tablero[c1]) > 0: # Queda al menos un elemento en c1
                self.tablero.move_to_empty_col(c1,c2)
                self.tablero.fix_col(c1, c2)
                #self.tablero.lejos(c2)
                return

        elif isinstance(self.tablero.columnas_de_tablero[c2][-1], list): # Si el último elemento de c2 es una lista:
            carta2 = self.tablero.columnas_de_tablero[c2][-1][-1] # última carta de la columna
            lista_carta2 = self.tablero.columnas_de_tablero[c2][-1] # lista donde está carta2 Y último elemento de c2
        else:
            carta2 = self.tablero.columnas_de_tablero[c2][-1] # Último elemento de c2
            lista_carta2 = None

        if isinstance(self.tablero.columnas_de_tablero[c1][-1], list): # c1 es una lista
            carta1 = self.tablero.columnas_de_tablero[c1][-1][-1] # carta1 es la última carta dentro de la lista
            if carta1.palo == carta2.palo: # Mismo palo

                for indice_carta, cada_carta in enumerate(self.tablero.columnas_de_tablero[c1][-1]):
                    if cada_carta.valor == carta2.valor-1: # un valor de c1 encaja con c2
                        if indice_carta == 0:
                            pass
                        elif indice_carta >0:
                            self.tablero.prepare_list(c1,indice_carta)
                        if not lista_carta2 is None: # el último elemento de c2 es una lista
                            self.tablero.move_list_to_list(c1,c2,True)

                        elif lista_carta2 is None: # el último elemento de c2 es una carta
                            self.tablero.move_list_to_card(c1,c2,True)

                        self.tablero.fix_col(c1, c2)
                        return

            else: # c1 lista, distintos palos
                for i, carta in enumerate(self.tablero.columnas_de_tablero[c1][-1]):
                    if carta.valor == carta2.valor-1:
                        if i == 0:
                            pass
                        elif i > 0:
                            self.tablero.prepare_list(c1,i)
                        self.tablero.move_list_to_card(c1,c2,False)
                        self.tablero.fix_col(c1,c2)

        else: # c1 es una carta
            carta1 = self.tablero.columnas_de_tablero[c1][-1]
            if carta1.valor == carta2.valor-1:
                if carta1.palo == carta2.palo:

                    if not lista_carta2 is None:  # el último elemento de c2 es una lista
                        self.tablero.move_card_to_list(c1, c2, True)
                        self.tablero.fix_col(c1, c2)

                    elif lista_carta2 is None:  # el último elemento de c2 es una carta
                        self.tablero.move_card_to_card(c1, c2, True)
                        self.tablero.fix_col(c1, c2)

                else:# c1 es una carta, distintos palos
                    self.tablero.move_card_to_card(c1,c2,False)
                    self.tablero.fix_col(c1,c2)
        print()

def main():
    juego = Juego()
    juego.crear_cartas()
    juego.mezclar()
    juego.repartir_a_tablero()
    juego.repartir_a_mazo()
    return juego

if __name__ == "__main__":
    juego = main()
    juego.tablero.update_columnas_de_tablero()