from maple.dll_manager import gcd_, isprime_, rem_, phi_


def gcd(num1: int, num2: int) -> int:
    num1 = str(num1)
    num2 = str(num2)
    res = gcd_(
        num1.encode(encoding="utf8"),
        num2.encode(encoding="utf8")
    )
    return int(res)


def is_prime(num: int) -> int:
    num = str(num)
    res = isprime_(num.encode(encoding="utf8"))
    return int(res)


def prevprime(n: int) -> int:
    n = int(n)
    if n < 2:
        return 2
    prime = n if n % 2 != 0 else n - 1
    while not is_prime(prime):
        prime -= 2
    return prime


def nextprime(n: int) -> int:
    if n < 2:
        return 2
    prime = n if n % 2 != 0 else n + 1
    while not is_prime(prime):
        prime += 2
    return prime


def rem(param_n: int, param_m: int, param_b: int) -> int:
    if param_m < 0:
        param_n = param_n**abs(param_m)
        return modinv(param_n, param_b)
    n = str(param_n)
    m = str(param_m)
    b = str(param_b)
    res = rem_(
        n.encode(),
        m.encode(),
        b.encode()
    )
    return int(res)


def phi(n: int) -> int:
    n = str(n)
    res = phi_(n.encode(encoding="utf8"))
    return int(res)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a: int, m: int) -> int:
    a = int(a)
    m = int(m)
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
