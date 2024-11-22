class NotPrimeNumber(Exception):
    pass

# RSA CIPHER
def encode(message: str, open_key: int, mod: int):  #функция принимает строку message, открытый ключ open_key и модуль mod.
    symbols = []
    for sym in message:                             #преобразует каждый символ сообщения в его ASCII-код с помощью ord(sym) шифрует
        symbols.append(ord(sym))                    #этот код с помощью функции cipher и собирает зашифрованные значения в строку 
    string = ''                                    
    for sym in symbols:
        string += str(cipher(sym, open_key, mod)) + ' '
    return string[:-1]                              #Возвращает строку, содержащую зашифрованные значения, разделенные пробелами.

def decode(message: str, secret_key: int, mod: int):#функция принимает зашифрованное сообщение message, закрытый ключ secret_key и модуль mod.
    symbols = message.split(' ')                    #разбивает строку на отдельные зашифрованные символы, расшифровывает каждый из них 
    string = ''                                     
    for sym in symbols:
        string += chr(cipher(int(sym), secret_key, mod))#с помощью функции cipher и собирает расшифрованные символы в строку.
    return string

def cipher(symbol: int, key: int, mod: int): 
    return pow(symbol, key, mod)                     #возведения в степень по модулю


# RSA GET KEYS
ferma = [65537, 257, 17, 5, 3]

def generate_keys(p: int, q: int):  #генерирует открытый и закрытый ключи.
    if not is_prime(p) or not is_prime(q):
        raise NotPrimeNumber
    n = p*q
    euler = (p-1)*(q-1)             #Находит открытый ключ e, который является взаимно простым с euler, и закрытый ключ d
    e = get_coprime(euler)          #который является модульным обратным к e по модулю euler.
    d = get_modulo_inverse(e, euler)
    return e, d, n                  #Возвращаем открытый ключ e, закрытый ключ d и модуль n.

def is_prime(num: int):             #Проверяем, является ли число num простым.
    if num % 2 == 0:
        return num == 2
    d = 3
    while d * d <= num and num % d != 0:
        d += 2
    return d * d > num

def get_coprime(num: int):          #Находим первое число из списка ferma, которое является взаимно простым с num.
    for n in ferma:
        if gcd(num, n) == 1:
            return n

def gcd(p: int, q: int):            #Вычисляем наибольший общий делитель (НОД) двух чисел p и q с помощью алгоритма Евклида.
    while q != 0:
        p, q = q, p % q
    return p

def get_modulo_inverse(a: int, m: int): #Находиv модульный обратный элемент a по модулю m
    return pow(a, -1, m)