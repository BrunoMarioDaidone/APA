"""
Bruno Mario Daidone Rossini
Fichero con una clase y una función que generan 
números semialeatorios usando el algoritmo de generación
lineal congruente LGC.
"""

class Aleat:

    """
    Clase Aleat: generador de números pseudoaleatorios usando el método congruencial lineal (LGC).

    COMETIDO
    --------
    Esta clase implementa un generador de números pseudoaleatorios en el rango
    0 ≤ x_n < m mediante la fórmula:

        x_{n+1} = (a * x_n + c) mod m

    Permite generar secuencias deterministas y reiniciables mediante una nueva semilla.

    ATRIBUTOS
    ---------
    m : int
        Módulo del generador (define el rango de valores).
    a : int
        Multiplicador del generador.
    c : int
        Incremento del generador.
    x : int
        Estado actual de la secuencia (último valor generado).

    MÉTODOS
    -------
    __init__(m, a, c, x0)
        Inicializa el generador con los parámetros dados (por clave obligatoriamente).

    __iter__()
        Devuelve el propio objeto como iterador.

    __next__()
        Genera y devuelve el siguiente número pseudoaleatorio.

    __call__(seed)
        Reinicia la secuencia usando la semilla indicada.

    PRUEBAS UNITARIAS (doctest)
    ----------------------------

    Comprobación del funcionamiento de Aleat:
    >>> rand = Aleat(m=32, a=9, c=13, x0=11)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    16
    29
    18
    15

    Comprobación del reinicio de Aleat:
    >>> rand(29)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    18
    15
    20
    1
    """

    def __init__(self, *, m=2**48, a=2521490317, c=11, x0=1212121):
        self.m = m
        self.a = a
        self.c = c 
        self.x = x0

    def __iter__(self):
        return self

    def __next__(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def __call__(self, seed):
        self.x = seed  



def aleat(m=2**48, a=2521490317, c=11, x0=1212121):

    """
    Función generadora aleat: generador de números pseudoaleatorios basado en el método congruencial lineal (LGC).

    COMETIDO
    --------
    Genera una secuencia de números pseudoaleatorios en el rango 0 ≤ x_n < m
    utilizando la fórmula:

        x_{n+1} = (a * x_n + c) mod m

    Es una función generadora que produce valores de forma iterativa mediante yield
    y permite reiniciar la secuencia mediante send().

    ARGUMENTOS
    ----------
    m : int (opcional)
        Módulo del generador. Define el rango de valores [0, m).
    a : int (opcional)
        Multiplicador del generador.
    c : int (opcional)
        Incremento del generador.
    x0 : int (opcional)
        Semilla inicial de la secuencia.

    SALIDA
    ------
    yield int
        Devuelve en cada iteración el siguiente número pseudoaleatorio generado.

    PRUEBAS UNITARIAS (doctest)
    ----------------------------

    Comprobación del funcionamiento de aleat():
    >>> rand = aleat(m=64, a=5, c=46, x0=36)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    34
    24
    38
    44

    Comprobación del reinicio de aleat():
    >>> _ = rand.send(24)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    44
    10
    32
    14
    """

  x = x0

    while True:
        x = (a * x + c) % m
        nuevo = yield x
        if nuevo is not None:
            x = nuevo


import doctest
doctest.testmod()