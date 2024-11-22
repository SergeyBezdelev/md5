import math

class MD5:
                                                    #принимаем строку message и возвращаем её MD5-хеш в виде байтов.
    def encode(self, message: str) -> bytes:        #массив из 64 элементов, который содержит константы, вычисляемые с использованием синуса. 
        self.T = [int(2 ** 32 * abs(math.sin(i+1))) for i in range(64)] #константы используются в процессе хеширования для обеспечения разнообразия.
        self.message = message                      #сохраняет входное сообщение.
        self.__step_one()
        self.__step_two()
        result = self.__step_four()
        return result           #возвращает результат, который будет представлять собой хеш.
    
    def __step_one(self) -> None:                                   #метод подготавливает сообщение для хеширования. Выравнивание потока+добавление длинны сообщения
        self.len_of_message = (8 * len(self.message)) % pow(2, 64)  #вычисляем длину сообщения в битах и сохраняет её. Это значение будет
        self.message = bytearray(self.message.encode('utf-8'))      #добавлено в конце сообщения, преобразует строку в байтовый массив
        
        self.message.append(0x80)           #добавляет байт, который указывает на конец сообщения
        while len(self.message) % 64 != 56: #добавляет нули в массив до тех пор, пока его длина не станет равной 56 байтам 
            self.message.append(0x00)       #Это необходимо для того, чтобы в конце сообщения можно было добавить длину.
    
    def __step_two(self) -> None: #метод добавляет длину сообщения в конец подготовленного массива
        self.message += self.len_of_message.to_bytes(8, 'little')
    
    def __left_rotate(self, a, b):#метод выполняет циклический сдвиг влево для 32-битного целого числа.
        a &= 0xFFFFFFFF
        return ((a<<b) | (a>>(32-b))) & 0xFFFFFFFF
        
    def __step_four(self) -> bytes:
        A0 = 0x67452301          #инициализация буфера
        B0 = 0xefcdab89          #начальные значения для четырех 32-битных переменных
        C0 = 0x98badcfe
        D0 = 0x10325476
        A, B, C, D = A0, B0, C0, D0
        for i in range(0, len(self.message), 64):#Цикл проходит по сообщению, обрабатывая его блоками по 64 байта
            X = [int.from_bytes(self.message[i:i+4], byteorder='little') for i in range(i, i+64, 4)]#массив из 16 32-битных слов
            for iter in range(64):      #Вычисление хеша
                if iter < 16:
                    k = iter            #индекс, который указывает, какое слово из массива X будет использоваться в данной итерации.
                    s = [7, 12, 17, 22] #массив сдвигов, который определяет, на сколько битов будет выполнен циклический сдвиг.
                    func = self.__F(B, C, D)
                elif iter < 32:
                    k = ((5 * iter) + 1) % 16
                    s = [5, 9, 14, 20]
                    func = self.__G(B, C, D)
                elif iter < 48:
                    k = ((3 * iter) + 5) % 16
                    s = [4, 11, 16, 23]
                    func = self.__H(B, C, D)
                elif iter < 64:
                    k = (7 * iter) % 16
                    s = [6, 10, 15, 21]
                    func = self.__I(B, C, D)
                new_B = (B + self.__left_rotate(A + func + X[k] + self.T[iter], s[iter % 4])) & 0xFFFFFFFF
                A, B, C, D = D, new_B, B, C
            A0 = (A0 + A) & 0xFFFFFFFF
            B0 = (B0 + B) & 0xFFFFFFFF
            C0 = (C0 + C) & 0xFFFFFFFF                      #перестановка байт в переменных ABCD
            D0 = (D0 + D) & 0xFFFFFFFF
                                                            # Преобразует 32-битное целое число A0 в байтовое представление длиной 4
        result = bytearray(A0.to_bytes(4, byteorder='little'))#байта в формат что младший байт будет первым
        result.extend(B0.to_bytes(4, byteorder='little'))   #Добавляет байтовое представление B0 к массиву result
        result.extend(C0.to_bytes(4, byteorder='little'))   #Добавляет байтовое представление C0
        result.extend(D0.to_bytes(4, byteorder='little'))   #Добавляет байтовое представление D0
        return result.hex()     #Преобразует байтовый массив result в строку шестнадцатеричного представления и возвращает её.
                    
    def __F(self, b: int, c: int, d: int) -> bool:

        return (b & c) | (~b & d)               #возвращает биты и объединяет результаты

    def __G(self, b: int, c: int, d: int) -> bool:
        return (d & b) | (~d & c)               #возвращает биты и объединяет результаты

    def __H(self, b: int, c: int, d: int) -> bool:
        return b ^ c ^ d                        #возвращает побитовую операцию "исключающее ИЛИ" (XOR) для b, c и d
    
    def __I(self, b: int, c: int, d: int) -> bool:
        return c ^ (b | ~d)                     #возвращает биты, которые установлены в b или не установлены в d