class Point:
    """
    Класс, представляющий точку на эллиптической кривой.

    Attributes:
        x: int Координата x точки.
        y: int Координата y точки.
        is_infty: bool Флаг, указывающий,
        является ли точка бесконечной.

    Methods:
        __repr__: Возвращает строковое представление точки.
        __eq__: Проверяет равенство двух точек.
        __ne__: Проверяет неравенство двух точек.
    """
    def __init__(
            self,
            x: int or None,
            y: int or None,
            is_infty=False
    ):
        """
        Инициализация объекта Point.

        Args:
            x: int Координата x точки.
            y: int Координата y точки.
            is_infty: bool Флаг, указывающий,
            является ли точка бесконечной.
        """
        if is_infty:
            self.is_infty = True
            x = None
            y = None
        else:
            self.is_infty = False
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        """
        Возвращает строковое представление точки.

        Returns:
            str: Строковое представление точки.
        """
        return "x: " + str(self.x) + "  " + "y: " + str(self.y)

    def __eq__(self, other: "Point") -> bool:
        """
        Проверяет равенство двух точек.

        Args:
            other (Point): Другая точка для сравнения.

        Returns:
            bool: True, если точки равны, иначе False.
        """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Point") -> bool:
        return not self.__eq__(other)