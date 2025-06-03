class Carta:
    def __init__(self, valor, palo, oculta=True, in_game=True, carta_encima=True):
        self.valor = valor
        self.palo = palo
        self.oculta = oculta
        self.carta_encima = carta_encima
        self.in_game = in_game

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.oculta:
            return " █ "
        else:
            if self.valor == 1:
                return f'A{self.palo}'
            elif self.valor == 11:
                return f'J{self.palo}'
            elif self.valor == 12:
                return f'Q{self.palo}'
            elif self.valor == 13:
                return f'K{self.palo}'
            else:
                return f'{self.valor}{self.palo}'

    def mostrar(self):
        self.oculta = False

    def fuera_de_juego(self):
        self.in_game = False