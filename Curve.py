from maple.maple import rem


class Point:
    """
    Класс, представляющий точку на эллиптической кривой.

    Attributes:
        x (int): Координата x точки.
        y (int): Координата y точки.
        is_infty (bool): Флаг, указывающий, является ли точка бесконечной.

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
            x (int): Координата x точки.
            y (int): Координата y точки.
            is_infty (bool): Флаг, указывающий,
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


class Curve:
    """
    Класс, представляющий эллиптическую
    кривую для использования в криптографии.
    """
    def __init__(self, a: int, b: int, G: Point, p: int):
        """
        Инициализация объекта Curve.

        Args:
            a (int): Параметр кривой.
            b (int): Параметр кривой.
            G (Point): Генераторная точка на кривой.
            p (int): Простое число, модуль для операций по модулю.
        """
        self.a = a
        self.b = b
        self.G = G
        self.p = p

    def add(self, point1: Point, point2: Point) -> Point:
        """
        Сложение двух точек на эллиптической кривой.

        Args:
            point1 (Point): Первая точка.
            point2 (Point): Вторая точка.

        Returns:
            Point: Результат сложения точек.
        """
        # handle special case for point at infinity
        if point2.is_infty:
            return point1
        if point1.is_infty:
            return point2

        if point1 == point2:
            # calculate (3x_1**2 + a)/(2y_1) mod p
            l = ((3 * rem(point1.x, 2, self.p) + self.a) *
                 rem((2 * point1.y % self.p), -1, self.p))
        else:
            # calculate (y_2 - y_1)/ (x_2 - x_1) mod p
            l = (((point2.y - point1.y) % self.p) *
                 rem(((point2.x - point1.x) % self.p), -1, self.p))
        x_res = (rem(l, 2, self.p) - point1.x - point2.x) % self.p
        y_res = (l * (point1.x - x_res) - point1.y) % self.p
        return Point(x_res, y_res)

    def double_and_add(self, point: Point, n: int) -> Point:
        """
        Удвоение и сложение точек на эллиптической кривой.
        Args:
            point (Point): Точка, которую нужно удвоить и сложить.
            n (int): Целочисленный множитель.
        Returns:
            Point: Результат удвоения и сложения.
        """
        acc = Point(None, None, True)  # start at point at infinity
        curr = point
        while n != 0:
            if n & 1 == 1:
                acc = self.add(acc, curr)
            curr = self.add(curr, curr)
            n = n >> 1
        return acc

    def ecdh(self, pub, priv):
        """
        Реализация алгоритма обмена ключами по эллиптической кривой (ECDH).

        Args:
            pub (Point): Публичный ключ другой стороны.
            priv (int): Приватный ключ текущей стороны.

        Returns:
            int: Общий секрет, вычисленный с использованием ECDH.
        """
        return self.double_and_add(pub, priv).x