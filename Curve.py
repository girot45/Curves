from Curves.Point import Point
from Curves.maple.maple import rem, is_prime
from Curves.utils import factorset
import random


class Curve:
    """
    Класс, представляющий эллиптическую
    кривую для использования в криптографии.
     Args:
            a (int): Параметр кривой.
            b (int): Параметр кривой.
            p (int): Простое число, модуль для операций по модулю.
    """

    def __init__(self, a: int, b: int, p: int):
        """
        Инициализация объекта Curve.

        Args:
            a (int): Параметр кривой.
            b (int): Параметр кривой.
            p (int): Простое число, модуль для операций по модулю.
        """
        self.a = a
        self.b = b
        self.p = p

    def ecdh(self, pub, priv):
        """
        Реализация алгоритма обмена ключами по эллиптической кривой (ECDH).

        Args:
            pub (Point): Публичный ключ другой стороны.
            priv (int): Приватный ключ текущей стороны.

        Returns:
            int: Общий секрет, вычисленный с использованием ECDH.
        """
        return self.ECC_Mult(pub, priv).x

    def ECC_Generator(self):
        """
        Генерация генератора группы точек эллиптической кривой.

        Returns:
            Point: Генератор группы точек эллиптической кривой.
        """
        setPoints = self.ECC_AllPoints()
        countPoints = len(setPoints) + 1
        rollIndex = random.randint(0, countPoints - 1)

        if is_prime(countPoints):
            x, y = setPoints[rollIndex]
            G = Point(x, y)
        else:
            setDivs = factorset(countPoints)
            countDivs = len(setDivs)
            n = setDivs[countDivs - 1]
            h = countPoints // n
            i = 0
            G = Point(0, 0)

            while G.x == 0 and G.y == 0 and i <= countPoints:
                x, y = setPoints[i]
                P = Point(x, y)
                G = self.ECC_Mult(P, h)
                i += 1

        if G.x == 0 and G.y == 0:
            print("!Эллиптическая кривая выбрана плохо.")
            print("!Подберите другие параметры кривой.")

        return G

    def ECC_Add(self, point1: Point, point2: Point) -> Point:
        """
        Сложение двух точек на эллиптической кривой.
        Args:
            point1 (Point): Первая точка.
            point2 (Point): Вторая точка.
        Returns:
            Point: Результат сложения точек.
        """
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        x3, y3 = 666, 666

        if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
            if x1 == 0 and y1 == 0:
                x3 = x2 % self.p
                y3 = y2 % self.p
            else:
                x3 = x1 % self.p
                y3 = y1 % self.p
        else:
            if x1 == x2 and y1 == y2:
                if y1 != 0:
                    lambda_val = (
                            (3 * x1 ** 2 + self.a) *
                            rem(2 * y1, -1, self.p) % self.p)
                    x3 = (lambda_val ** 2 - x1 - x1) % self.p
                    y3 = (lambda_val * (x1 - x3) - y1) % self.p
                else:
                    x3, y3 = 0, 0
            elif x1 != x2 or y1 != y2:
                if x1 != x2:
                    lambda_val = ((y2 - y1) *
                                  rem(x2 - x1, -1, self.p) % self.p)
                    x3 = (lambda_val ** 2 - x1 - x2) % self.p
                    y3 = (lambda_val * (x1 - x3) - y1) % self.p
                else:
                    x3, y3 = 0, 0

        return Point(x3, y3)

    def ECC_Sub(self, P: Point, Q: Point) -> Point:
        """
        Вычитание двух целочисленных точек на эллиптической кривой в поле Галуа
        Args:
            P: Point - Первая точка.
            Q: Point - Вторая точка.
        Returns:
            Point: Результат разности точек.
        """
        tempQ = Point(Q.x, -Q.y % self.p)
        R = self.ECC_Add(P, tempQ)
        return R

    def ECC_Mult(self, P: Point, k: int) -> Point:
        """
        Умножение целочисленной точки на целое число
        на эллиптической кривой в поле Галуа
        Args:
            P: Point - точка
            k: int - множитель
        Returns:
            Point: Результат умножения точки на число
        """

        def count_Q(tempk):
            Q_ = Point(0, 0)
            i = 0
            num = bin(tempk)[2:]
            len_num = len(num)

            while i < len_num:
                Q_ = self.ECC_Add(Q_, Q_)
                if num[i] == "1":
                    Q_ = self.ECC_Add(Q_, P)
                i += 1
            return Q_

        if k >= 0:
            R = count_Q(k)
        else:
            Q = count_Q(-k)
            R = Point(Q.x, -Q.y % self.p)

        return R

    def ECC_AllPoints(self) -> list:
        """
        Поиск всех целочисленных точек
        на эллиптической кривой в поле Галуа
        Returns:

        """
        points = []
        for x in range(self.p):
            y_squared = (x ** 3 + self.a * x + self.b) % self.p
            y = rem(y_squared, (self.p + 1) // 4, self.p)

            if rem(y, 2, self.p) == y_squared:
                points.append([x, y])
                points.append([x, -y % self.p])
        return points

    def ECC_CountPoints(self):
        """
        Вычисление количества целочисленных точек,
        включая бесконечно удалённую,
        на эллиптической кривой в поле Галуа.
        Returns:
            count: int - количества целочисленных точек,
                включая бесконечно удалённую.
        """
        count = 1  # Первая точка - бесконечная
        for x in range(self.p):
            y_squared = (x ** 3 + self.a * x + self.b) % self.p
            y = rem(y_squared, (self.p + 1) // 4, self.p)
            if (y ** 2) % self.p == y_squared:
                count += 2
        return count

    def ECC_OrderPoint(self, P: Point) -> int:
        """
        Вычисление порядка точки на эллиптической кривой в поле Галуа
        Args:
            P: Point - точка на кривой
        Returns:
            n: int - порядок точки на кривой
        """
        countPoints = self.ECC_CountPoints()
        setDivs = factorset(countPoints)
        R = Point(115, 1665)
        i = 0

        while R.x != 0 or R.y != 0:
            i += 1
            R = self.ECC_Mult(P, setDivs[i - 1])

        n = setDivs[i - 1]
        return n
