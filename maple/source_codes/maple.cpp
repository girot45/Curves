#include "BigInt.hpp"
#include <iostream>
#include <cstring>
#include <random>

// Генератор случайных чисел
std::random_device rd;
std::mt19937 gen(rd());


BigInt func_Rem(
    const BigInt param_n,
    const BigInt param_m,
    const BigInt param_b
)
{
    if (param_m == 0)
    {
        return 1;
    }
    if (param_m % 2 == 0)
    {
        return func_Rem(
            (param_n * param_n) % param_b,
            param_m / 2,
            param_b
            );
    }
    else
    {
        return (
            param_n * func_Rem(
                (param_n * param_n) % param_b,
                (param_m - 1) / 2,
                 param_b
                 )
                 ) % param_b;
    }
}



bool check_witness(BigInt a, BigInt s, BigInt d, BigInt n)
{
    BigInt x = func_Rem(a, d, n);
    if (x == 1 || x == n - 1)
        return true;
    for (BigInt i = 0; i < s - 1; ++i)
    {
        x = (x * x) % n;
        if (x == n - 1)
            return true;
    }
    return false;
}

// Функция для теста простоты числа с использованием теста Миллера-Рабина
bool isPrime(BigInt num)
{
    int k = 5;
    if (num <= 1)
        return false;
    if (num <= 3)
        return true;
    if (num % 2 == 0 || num % 3 == 0)
        return false;

    BigInt s = 0, d = num - 1;
    while (d % 2 == 0)
    {
        s += 1;
        d /= 2;
    }

    for (int i = 0; i < k; ++i)
    {
        BigInt a = 2 + gen() % (num - 4); // Генерация случайного числа от 2 до num-2
        if (!check_witness(a, s, d, num))
            return false;
    }
    return true;
}

//// Функция для определения простое ли число
//bool isPrime(BigInt num)
//{
//    if (num <= 1)
//        return false;
//    if (num <= 3)
//        return true;
//    if (num % 2 == 0 or num % 3 == 0)
//        return false;
//    for (BigInt i = 5; i * i <= num; i += 6)
//    {
//        if (num % i == 0 || num % (i + 2) == 0)
//            return false;
//    }
//    return true;
//}




extern "C" __declspec(dllexport) 
 const char* gcd(const char* str1, const char* str2)
 /*
    Экспорт функция для реализации 
    вычисления наибольшего общего делителя
 */
{
    BigInt num1, num2, result;
    num1 = str1;
    num2 = str2;
	result = gcd(num1, num2);

    
	std::string result_str = result.to_string();
    return strdup(result_str.c_str());
}


extern "C" __declspec(dllexport) 
 bool isprime(const char* str1)
 /*
    Экспорт функция для определения простое ли число
 */
{
    BigInt num;
    num = str1;
    return isPrime(num);	 
}



extern "C" __declspec(dllexport) 
 const char* rem(
        const char* str1,
        const char* str2,
        const char* str3
 )
 /*
    Функция экспорт для вычисления 
    возведения числа в степень по модулю
 */
{
    BigInt num1, num2, num3, result;
    num1 = str1;
    num2 = str2;
    num3 = str3;
	result = func_Rem(num1, num2, num3);
    
    std::string result_str = result.to_string();
    return strdup(result_str.c_str());
}


extern "C" __declspec(dllexport) 
 const char* phi(const char* str1)
 /*
    Экспорт функция для вычисления 
    значения алгоритма Евклида
 */
{
    BigInt num, result;
    num = str1;
    
    if (num <= 0) {
        return 0;
    }

    result = num;

    for (BigInt i = 2; i * i <= num; ++i) {
        if (num % i == 0) {
            while (num % i == 0) {
                num /= i;
            }
            result -= result / i;
        }
    }

    if (num > 1) {
        result -= result / num;
    }


    std::string result_str = result.to_string();
    return strdup(result_str.c_str());
}


