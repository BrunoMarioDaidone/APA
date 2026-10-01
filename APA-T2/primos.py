"""
Bruno Mario Daidone Rossini
"""

def esPrimo(numero):

    """
    Función que devuelve True si el argumento es
    primo, y False si no lo es.

    >>> [numero for numero in range(2, 50) if esPrimo(numero)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """

    if numero < 2:
        return False


    i=2
    for i in range(2, numero):
        if numero % i == 0:
            return False
    
    return True


def primos(numero):

    """
    Función que devuelve una tupla con todos los numeros 
    primos menores al argumento (numero)

    >>> primos(50)
    (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
    """

    lis = []
    i = 2

    for i in range (2, numero):
        if esPrimo(i) == True:
            lis.append(i)
    
    tup = tuple(lis)
    return tup


def descompon(numero):

    """
    Función que devuelve una tupla con la descomposicion
    en factores primos de su argumento

    >>> descompon(36 * 175 * 143)
    (2, 2, 3, 3, 5, 5, 7, 11, 13)
    """

    i=2
    lis = []

    while i <= numero:
        if esPrimo(i) == True:
            if(numero % i == 0):
                lis.append(i)
                numero = numero // i
            else:
                i += 1
        else:
             i += 1
    
    tup = tuple(lis)
    return tup


def mcm(numero1, numero2):

    """
    Función que devuelve el mínimo común múltiplo
    de sus argumentos.

    >>> mcm(90, 14)
    630
    """

    factores1 = list(descompon(numero1))
    factores2 = list(descompon(numero2))

    resultado = 1

    factores2_copy = factores2.copy()
    
    resultado *= f
    if f in factores2_copy:
        factores2_copy.remove(f) 

    for f in factores2_copy:
        resultado *= f

    return resultado


def mcd(numero1, numero2):

    """
    Función que devuelve el máximo común divisor
    de sus argumentos.

    >>> mcd(924, 780)
    12
    """

    factores1 = list(descompon(numero1))
    factores2 = list(descompon(numero2))

    resultado = 1

    for f in factores1:
        if f in factores2:
            resultado *= f
            factores2.remove(f)  

    return resultado


def mcm(*numeros):
    """
    Calcula el mínimo común múltiplo de un número arbitrario de argumentos.

    >>> mcm(42, 60, 70, 63)
    1260
    """

    resultado = numeros[0]

    for n in numeros[1:]:
        factores1 = list(descompon(resultado))
        factores2 = list(descompon(n))

        temp = 1
        factores2_copy = factores2.copy()

        for f in factores1:
            temp *= f
            if f in factores2_copy:
                factores2_copy.remove(f)

        for f in factores2_copy:
            temp *= f

        resultado = temp

    return resultado


def mcd(*numeros):
    """
    Calcula el máximo común divisor de un número arbitrario de argumentos.

    >>> mcd(840, 630, 1050, 1470)
    210
    """

    resultado = numeros[0]

    for n in numeros[1:]:
        factores1 = list(descompon(resultado))
        factores2 = list(descompon(n))

        temp = 1
        for f in factores1:
            if f in factores2:
                temp *= f
                factores2.remove(f)

        resultado = temp

    return resultado

if __name__ == "__main__":
    import doctest
    doctest.testmod()
