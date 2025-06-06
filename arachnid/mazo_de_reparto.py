class MazoDeReparto:
    def __init__(self, empty=False):
        self.repartos_restantes = 0 # atributo que muestra cuántas cartas quedan para repartir.
        self.cartas_de_reparto = [] # acá se almacenan las cartas.
        self.empty = empty # bool, se activa cuando no quedan cartas para repartir.

    def guardar_cartas_a_repartir(self, cartas): # cartas tiene que ser una lista de objetos, cartas con sus atributos.
        for carta in cartas:
            self.cartas_de_reparto.append(carta)
        self.repartos_restantes = len(self.cartas_de_reparto) /10

    def repartiendo(self):
        if self.empty:
            print("Ya no quedan más cartas para repartir!")
            return
        else:
            to_show = self.cartas_de_reparto[-10:]
            self.cartas_de_reparto = self.cartas_de_reparto[:-10]
            for carta in to_show:
                carta.mostrar()
            self.repartos_restantes = len(self.cartas_de_reparto) / 10
            print(f"Repartos restantes= {int(self.repartos_restantes)}")
            if self.repartos_restantes == 0:
                self.bloquear()
            return to_show

    def bloquear(self):
        self.empty = True