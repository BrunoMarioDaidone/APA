class Vector:
    """
    Bruno Mario Daidone Rossini

    >>> v1 = Vector([1, 2, 3])
    >>> v2 = Vector([4, 5, 6])

    Multiplicación por escalar:
    >>> v1 * 2
    Vector([2, 4, 6])

    Producto de Hadamard:
    >>> v1 * v2
    Vector([4, 10, 18])
    
    Producto escalar:    
    >>> v1 @ v2
    32
    
    Prueba de componentes paralela y perpendicular.

    >>> v1 = Vector([2, 1, 2])
    >>> v2 = Vector([0.5, 1, 0.5])

    Componente paralela:
    >>> v1 // v2
    Vector([1.0, 2.0, 1.0])

    Componente perpendicular:
    >>> v1 % v2
    Vector([1.0, -1.0, 1.0])

    """

    vector = []
    vector = list()

    def __int__(self, iterable):
        """
        Constructor alternativo (incorrecto) que intenta crear un vector
        a partir de un iterable. No se usa normalmente.
        """
        self.vector = [expreson for elemento in iterable]

    def __init__(self, iterable=None):

        """
        Constructor principal de la clase Vector.
        Recibe un iterable y almacena sus valores como lista interna.

        >>> Vector([1, 2, 3])
        Vector([1, 2, 3])
        """
        self.vector = [valor for valor in iterable]

    def __repr__(self):
        """
        Representación oficial del vector, útil para depuración.
        Devuelve una cadena del tipo: Vector([1, 2, 3])
        """
        return 'Vector(' + repr(self.vector) + ')'

    def __str__(self):
        """
        Representación informal del vector, pensada para impresión.
        """
        return str(self.vector)

    def __getitem__(self, key):
        """
        Permite acceder a un elemento del vector mediante índices.

        >>> v = Vector([10, 20, 30])
        >>> v[1]
        20
        """
        return self.vector[key]

    def __setitem__(self, key, value):
        """
        Permite modificar un elemento del vector mediante índices.

        >>> v = Vector([1, 2, 3])
        >>> v[1] = 99
        >>> v
        Vector([1, 99, 3])
        """
        self.vector[key] = value
    
    def __len__(self):
        """
        Devuelve la longitud del vector.

        >>> len(Vector([1, 2, 3]))
        3
        """
        return len(self.vector)

    def __mul__(self, other):
        """
        Sobrecarga del operador *.
        Si 'other' es un número, realiza multiplicación por escalar.
        Si 'other' es otro vector, realiza el producto de Hadamard.
        """

        if isinstance(other, (int, float, complex)):
            return Vector(uno * other for uno in self)
        else:
            return Vector(uno * otro for uno, otro in zip(self, other))


    def __rmul__(self, other):
        """
        Multiplicación por la izquierda.
        Permite expresiones como: 2 * Vector([1, 2, 3])
        """
        return self.__mul__(other)
        
    def __matmul__(self, other):
        """
        Producto escalar entre dos vectores usando el operador @.
        """
        return sum(a * b for a, b in zip(self.vector, other.vector))

    def __rmatmul__(self, other):
        """
        Producto escalar por la izquierda.
        Permite expresiones como: v @ w o w @ v indistintamente.
        """
        return self.__matmul__(other)

    def __floordiv__(self, other):
        """
        Proyección del vector actual sobre otro vector usando //.
        Calcula: (self·other / other·other) * other
        """
        escalar = (self @ other) / (other @ other)
        return Vector([escalar * x for x in other.vector])

    def __rfloordiv__(self, other): 
        """
        Proyección por la izquierda.
        Permite calcular la proyección cuando el vector aparece
        a la derecha del operador //, es decir: u // v.
        """
        return other.__floordiv__(self)

    def __mod__(self, other):
        """
        Devuelve la componente normal de este vector respecto a 'other'.
        Es decir: v % u = v - proyección_de_v_sobre_u.
        """
        proy = self // other
        return Vector(a - b for a, b in zip(self.vector, proy.vector))

    def __rmod__(self, other):
        """
        Permite calcular la componente normal cuando el vector aparece
        a la derecha del operador %, es decir: u % v.
        """
        return other.__mod__(self)

if __name__ == "__main__":
    import doctest
    doctest.testmod()