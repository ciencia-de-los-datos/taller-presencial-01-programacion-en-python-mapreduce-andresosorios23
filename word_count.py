#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#

import os, re, fileinput, glob


def load_input(input_directory: str) -> list[tuple[str, str]]:
    files: list[str] = glob.glob(f"{input_directory}/*.txt")
    output: list[tuple[str, str]] = []
    for line in fileinput.input(files):
        output.append((fileinput.filename(), line))
    return output


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence: list[tuple[str, str]]) -> list[tuple[str, int]]:
    output: list[tuple[str, int]] = []
    for _, item in sequence:
        words: list[str] = item.replace(" \n", "").lower().split(" ")
        for word in words:
            word: str = re.sub("[^A-Za-z0-9]+", "", word)
            output.append((word, 1))

    return output


#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence: list[tuple[str, int]]) -> list[tuple[str, int]]:
    sequence.sort(key=lambda x: x[0])
    return sequence


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence: list[tuple[str, int]]) -> list[tuple[str, int]]:
    result: dict[str, int] = {}
    for item in sequence:
        if item[0] in result:
            result[item[0]] += 1
        else:
            result[item[0]] = 1
    return list(result.items())


#
# Escriba la función create_ouptput_directory que recibe un nombre de directorio
# y lo crea. Si el directorio existe, la función falla.
#
def create_output_directory(output_directory: str) -> None:
    try:
        os.mkdir(output_directory)
    except:
        raise Exception


#
# Escriba la función save_output, la cual almacena en un archivo de texto llamado
# part-00000 el resultado del reducer. El archivo debe ser guardado en el
# directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory: str, sequence: list[tuple[str, int]]):
    with open(os.path.join(output_directory, "part-00000"), "w") as file:
        lines: list[str] = []
        for item in sequence:
            lines.append(f"{item[0]}\t{item[1]}\n")
        file.writelines(lines)


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory: str):
    with open(os.path.join(output_directory, "_SUCCESS"), "w"):
        pass


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def job(input_directory: str, output_directory: str):
    output: list[tuple[str, str]] = load_input(input_directory=input_directory)
    output2: list[tuple[str, int]] = mapper(output)
    output2 = shuffle_and_sort(output2)
    output3: list[tuple[str, int]] = reducer(output2)
    create_output_directory(output_directory)
    save_output(output_directory, output3)
    create_marker(output_directory)


if __name__ == "__main__":
    job(
        "./input",
        "output",
    )
