from arachnid.juego import main
import sys
import pandas as pd
salir = ["salir", "sal", "s", "quit", "q", "exit", "e"]
salir2 = [word + "()" for word in salir]
def iniciar_juego():
    juego = main()
    columnas = juego.tablero.update_columnas_de_tablero()
    return juego, columnas

def instrucciones():
    print(f'''En el primer input;
    Ingresar el número de la columna donde está la carta o la lista de cartas que quieras mover,
en el segundo input; ingresa el número de la columna donde quieras moverla/s.
    
    También se pueden ingresar ambos dígitos en en el primer input, por ejemplo,
    "13" movería la carta en la columna 1, a la columna 3,
    solo si los valores de las cartas son adecuados.
    
    Podés ingresar r para repartir una fila de cartas.
    Y tenés varias palabras para salir:
    {salir}
    {salir2}
''')
def detectar_jugada(c1, c2, juego):
    # Repartir
    if c1 == "r":
        juego.repartir()
        return None, None  # Reinciar entradas

    # Caracteres inválidos.
    if not c1.isdigit() or len(c1) > 2:
        print("Entrada inválida. Ingresa 1 o 2 dígitos o 'r' para repartir.")
        return None, None

    # Jugada adecuada.
    if len(c1) == 2:
        if c1[0] == c1[1]:
            print("Debes ingresar dos columnas distintas.")
            return None, None
        try:
            col1, col2 = int(c1[0]), int(c1[1])
            juego.analizar(col1, col2)
            return None, None  # Jugada ejecutada, reiniciar entradas
        except ValueError:
            print("Dígitos inválidos.")
            return None, None

    if len(c1) == 1 and c1.isdigit():
        col1 = int(c1)
        if c2 == "":
            return col1, ""  # Falta c2
        elif not c2.isdigit() or len(c2) != 1:
            print("Ingresa solo un dígito como segunda columna.")
            return None, None
        else:
            col2 = int(c2)
            if col1 == col2:
                print("Debes elegir columnas distintas.")
                return None, None
            juego.analizar(col1, col2)
            return None, None

    print("Entrada inválida.")
    return None, None


def inicio():
    opciones={1:jugando, 2:instrucciones, 3:sys.exit}
    while True:
        print("Presiona '1' para iniciar juego.")
        print("Presiona '2' para ver las instrucciones.")
        print("Presiona '3' para salir")
        try:
            x = int(input("_"))
            if x in opciones:
                opciones[x]()
        except (ValueError, KeyError):
            print("Entrada no válida.")

def aplanar(col): # quita las listas dentro de cada columna para poder mostrarlas con pd
    resultado = []
    for item in col:
        if isinstance(item, list):
            resultado.extend(item)
        else:
            resultado.append(item)
    return resultado


def jugando():
    juego, columnas = iniciar_juego()
    
    while True:
        c1 = ""
        c2 = ""
        print("Se muestran las cartas:")
        columnas_aplanadas = [aplanar(col) for col in columnas]

        longitud_max = max(len(col) for col in columnas_aplanadas)

        for i in range(len(columnas_aplanadas)):
            while len(columnas_aplanadas[i]) < longitud_max:
                columnas_aplanadas[i].append("")

        df = pd.DataFrame({f'C_{i}': columnas_aplanadas[i] for i in range(len(columnas_aplanadas))})
        print(df)
        print("(Ingresa 'r' para repartir)")
        print()

        if c1 == "":
            c1 = input("carta/s en columna _ ")
            if c1 in salir or c1 in salir2:
                sys.exit()
        c1, c2 = detectar_jugada(c1, c2, juego)
        if c1 is not None and c2 == "":
            c2 = input("columna 2 _ ")
            if c2 in salir or c2 in salir2:
                sys.exit()
            c1, c2 = detectar_jugada(str(c1), str(c2), juego)

inicio()