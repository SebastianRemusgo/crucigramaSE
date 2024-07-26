import sys

from crucigrama import *


class CreadorCrucigrama():

    def __init__(self, crucigrama):
        """
        Crear un nuevo CSP (problema de satisfacción de restricciones) - crucigrama.
        """
        self.crucigrama = crucigrama
        self.dominios = {
            var: self.crucigrama.palabras.copy()
            for var in self.crucigrama.variables
        }

    def cuadricula_letras(self, asignacion):
        """
        Retornar una matriz (2D) representando una asignación dada.
        """
        letras = [
            [None for _ in range(self.crucigrama.ancho)]
            for _ in range(self.crucigrama.alto)
        ]
        for variable, palabra in asignacion.items():
            direccion = variable.direccion
            for k in range(len(palabra)):
                i = variable.i + (k if direccion == Variable.ABAJO else 0)
                j = variable.j + (k if direccion == Variable.DERECHA else 0)
                letras[i][j] = palabra[k]
        return letras

    def print(self, asignacion):
        """
        Imprimir el crucigrama asignado al terminal.
        """
        letras = self.cuadricula_letras(asignacion)
        for i in range(self.crucigrama.alto):
            for j in range(self.crucigrama.ancho):
                if self.crucigrama.estructura[i][j]:
                    print(letras[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, asignacion, filename):
        """
        Guardar el crucigrama a un archivo imagen.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letras = self.cuadricula_letras(asignacion)

        # Crear un lienzo blanco
        img = Image.new(
            "RGBA",
            (self.crucigrama.ancho * cell_size,
             self.crucigrama.alto * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crucigrama.alto):
            for j in range(self.crucigrama.ancho):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crucigrama.estructura[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letras[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letras[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letras[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Aplique la consistencia de nodos y arcos y, a continuación, resuelva el CSP.
        """
        self.consistencia_nodo()
        self.ac3()
        return self.backtrack(dict())

    def consistencia_nodo(self):
        """
        Actualizar `self.dominios` de forma que cada variable sea nodo-consistente.
        (Elimina cualquier valor que sea inconsistente con las restricciones unarias de una variable;
        en este caso, la longitud de la palabra).
        """
        raise NotImplementedError

    def revisar(self, x, y):
        """
        Hacer que la variable `x` tenga consistencia de arco con la variable `y`.
        Para ello, elimine los valores de `self.dominios[x]` para los que no hay
        valor correspondiente posible para `y` en `self.dominios[y]`.

        Devuelve True si se ha hecho una revisión al dominio de `x`; devuelve
        False si no se ha hecho ninguna revisión.
        """
        raise NotImplementedError

    def ac3(self, arcs=None): #Visite https://en.wikipedia.org/wiki/AC-3_algorithm para conocer la historia
        """
        Actualizar `self.dominios` de tal manera que cada variable sea consistencia de arco.
        Si `arcs` es None, comienza con la lista inicial de todos los arcos del problema.
        Si no, usa `arcs` como lista inicial de arcos para hacer consistencia.

        Devuelve True si se cumple la consistencia de arcos y no hay dominios vacíos;
        devuelve False si uno o más dominios terminan vacíos.
        """
        raise NotImplementedError

    def asignacion_completa(self, asignacion):
        """
        Devuelve True si `asignacion` está completa (es decir, asigna un valor a cada
        variable crucigrama); devuelve False en caso contrario.
        """
        raise NotImplementedError

    def consistencia(self, asignacion):
        """
        Devuelve True si `asignacion` es consistencia (es decir, las palabras encajan en crucigrama
        sin caracteres conflictivos); devuelve False en caso contrario.
        """
        raise NotImplementedError

    def ordenar_valores_dominio(self, var, asignacion):
        """
        Devuelve una lista de valores en el dominio de `var`
        - Puede NO estar ordenada.
        - Puede estar ordenada por el número de valores que descartan para las variables vecinas (menor a mayor).
        """
        raise NotImplementedError

    def seleccionar_variable_no_asignada(self, asignacion):
        """
        Devuelve una variable no asignada que no forme ya parte de `asignacion`.
        - Puede seleccionar la siguiente variable no asignada.
        - Puede elegir la variable con el minimo número de valores restantes en el dominio.
        - Puede elegir la variable con el minimo número de valores restantes en el dominio; y
          si hay empate, elige la variable con el mayor grado.
        """
        raise NotImplementedError

    def backtrack(self, asignacion):
        """
        Usando la Búsqueda Backtrack, toma como entrada una asignación parcial para el
        crucigrama y devuelve una asignación completa si es posible hacerlo.

        `asignacion` es un mapeo de variables (claves) a palabras (valores).

        Si no es posible la asignación, devuelve None.
        """
        raise NotImplementedError


def main():

    # Verificar parametros
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py estructura palabras [output]")

    # Parseo de los argumentos
    estructura = sys.argv[1]
    palabras = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generar el crucigrama
    crucigrama = Crucigrama(estructura, palabras)
    creador = CreadorCrucigrama(crucigrama)
    asignacion = creador.solve()

    # Print result
    if asignacion is None:
        print("No solution.")
    else:
        creador.print(asignacion)
        if output:
            creador.save(asignacion, output)

if __name__ == "__main__":
    main()