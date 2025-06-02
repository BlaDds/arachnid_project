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

    def crear_cartas(self): # creates
        for cantidad in range(8): # Crea 8 juegos completos de cartas. (Juego de carta: desde A hasta K)
            for _ in range(1,14): # Valores de carta, desde 1 a 13
                if cantidad % 2 == 0:# Crea 4 juegos completos del palo de carta ♥, y 4 juegos completos de ♦
                    self.baraja_de_inicio.append(Carta(valor=_, palo="♥")) # El palo se puede cambiar a gusto
                else:
                    self.baraja_de_inicio.append(Carta(valor=_, palo="♦")) # El palo se puede cambiar a gusto

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
            self.mostrando(estas)
        else:
            return


    def mostrando(self, cartas): # Muestra las cartas que se han repartido. Hace posible la creación de listas dentro de las propias columnas para mostrar el progreso de cartas adecuadas 0: [6♦, ♥5, 4♦, 3♥,[3♦, 2♦, 1♦, A♦]]
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
            print("Ingresa un valor para c1")
            return
        elif not isinstance(c2,int):
            print("ingresa un valor para c2")
            return

        carta2 = 0
        a_mover = []
        lista_carta2 = []
        if len(self.tablero.columnas_de_tablero[c1]) == 0:
            return
        if len(self.tablero.columnas_de_tablero[c2]) == 0: # c2 está vacío, nada para analizar, se mueve c1 a c2
            if len(self.tablero.columnas_de_tablero[c1]) > 0:
                mover_esto = self.tablero.columnas_de_tablero[c1].pop()
                self.tablero.columnas_de_tablero[c2].append(mover_esto)
                try:
                    self.tablero.columnas_de_tablero[c1][-1].mostrar()
                except AttributeError:
                    pass
                except IndexError:
                    pass
                return
            elif len(self.tablero.columnas_de_tablero[c1]) == 0: # c1 está vacío, no hay nada para mover
                return

        elif isinstance(self.tablero.columnas_de_tablero[c2][-1], list): # Si el último elemento de c2 es una lista:
            carta2 = self.tablero.columnas_de_tablero[c2][-1][-1] # última carta de la columna
            lista_carta2 = self.tablero.columnas_de_tablero[c2][-1] # lista donde está carta2 Y último elemento de c2
        else:
            carta2 = self.tablero.columnas_de_tablero[c2][-1] # Último elemento de c2
            lista_carta2 = None

        if isinstance(self.tablero.columnas_de_tablero[c1][-1], list): # c1 es una lista
            carta1 = self.tablero.columnas_de_tablero[c1][-1][-1] # carta1 es la última carta dentro de la lista
            if carta1.palo == carta2.palo: # Mismo palo, se crea un juego (una lista) con esas cartas
                for i, cada_carta in enumerate(self.tablero.columnas_de_tablero[c1][-1]):
                    if cada_carta.valor == carta2.valor-1 :
                        a_mover = self.tablero.columnas_de_tablero[c1][-1][i:]

                        self.tablero.columnas_de_tablero[c1][-1] = self.tablero.columnas_de_tablero[c1][-1][:i]
                        if len(self.tablero.columnas_de_tablero[c1][-1]) == 0:
                            self.tablero.columnas_de_tablero[c1].pop()
                        elif len(self.tablero.columnas_de_tablero[c1][-1]) == 1:
                            self.tablero.columnas_de_tablero[c1][-1] = self.tablero.columnas_de_tablero[c1][-1][0]


                        if len(a_mover) == 1:
                            a_mover = a_mover[0]
                            if not lista_carta2 is None: # c2 es una lista
                                lista_carta2.append(a_mover)
                                self.tablero.lejos(c2)
                            else:
                                carta_c2 = self.tablero.columnas_de_tablero[c2].pop()
                                self.tablero.columnas_de_tablero[c2].append([carta_c2, a_mover])
                                self.tablero.lejos(c2)
                        elif len(a_mover) > 1: # se mueve una lista de elementos (de c1 = [x,x,x,x], se mueve más de un elemento)
                            if not lista_carta2 is None: # c2 es una lista
                                for x in a_mover:
                                    lista_carta2.append(x)
                                self.tablero.lejos(c2)
                                try:
                                    self.tablero.columnas_de_tablero[c1][-1].mostrar()
                                except AttributeError:
                                    pass
                                except IndexError:
                                    pass

                            elif lista_carta2 is None:
                                cartac2 = self.tablero.columnas_de_tablero[c2].pop()
                                a_mover.insert(0,cartac2)
                                self.tablero.columnas_de_tablero[c2].append(a_mover)
                                self.tablero.lejos(c2)
                                try:
                                    self.tablero.columnas_de_tablero[c1][-1].mostrar()
                                except (AttributeError,IndexError):
                                    pass

            else: # c1 lista, c2 carta, distinto palo
                for i, carta in enumerate(self.tablero.columnas_de_tablero[c1][-1]):
                    if carta.valor == carta2.valor-1:
                        a_mover = self.tablero.columnas_de_tablero[c1][-1][i:]
                        self.tablero.columnas_de_tablero[c1][-1] = self.tablero.columnas_de_tablero[c1][-1][:i]
                if len(self.tablero.columnas_de_tablero[c1][-1]) == 1:
                    self.tablero.columnas_de_tablero[c1][-1] = self.tablero.columnas_de_tablero[c1][-1][0]
                elif len(self.tablero.columnas_de_tablero[c1][-1]) == 0:
                    self.tablero.columnas_de_tablero[c1].pop()

                if len(a_mover) == 1:
                    a_mover = a_mover[0]
                    self.tablero.columnas_de_tablero[c2].append(a_mover)

                elif len(a_mover) > 1:
                    self.tablero.columnas_de_tablero[c2].append(a_mover)

                elif len(a_mover) == 0:
                    pass




        else: # c1 es una carta
            carta1 = self.tablero.columnas_de_tablero[c1][-1]
            if carta2.valor == carta1.valor+1:
                if carta1.palo == carta2.palo:
                    carta1 = self.tablero.columnas_de_tablero[c1].pop()
                    try:
                        lista_carta2.append(carta1)
                        self.tablero.lejos(c2)
                    except AttributeError:
                        carta2 = self.tablero.columnas_de_tablero[c2].pop()
                        agregar = [carta2,carta1]
                        self.tablero.columnas_de_tablero[c2].append(agregar)
                        self.tablero.lejos(c2)
                        pass
                else:
                    popped = self.tablero.columnas_de_tablero[c1].pop()
                    self.tablero.columnas_de_tablero[c2].append(popped)
            else:
                pass


        try:
            self.tablero.columnas_de_tablero[c1][-1].mostrar()
        except AttributeError:
            pass
        except IndexError:
            pass

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