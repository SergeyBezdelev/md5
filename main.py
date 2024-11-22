from md5 import MD5
from RSA import generate_keys, encode, decode

class EDS:
    def __init__(self):
        self.public_key, self.secret_key, self.mod = generate_keys(31231, 34673)

    def __GenerateHash(self, file) -> str | None:        
        try:                                             #Метод принимает имя файла в качестве аргумента и открыветего для чтения
            with open(file, 'r', encoding='utf-8') as f: #Если файл успешно открыт, его содержимое считывается и передается в 
                content: str = f.read()                 
                return MD5().encode(content)             #функцию MD5().encode(content), которая возвращает MD5-хэш содержимого файла
        except FileNotFoundError:
            print("Файл не найден")

    def EncodeHash(self, file) -> str | None:                 #Метод принимает имя файла и вызывает __GenerateHash для получения хэша
        if (result := self.__GenerateHash(file)) is not None: #Если хэш успешно сгенерирован, происходит кодирование с использованием 
            return encode(result, self.public_key, self.mod)  #публичного ключа и происходит возвращение закодированного хэша.
    
    def DecodeHash(self, file, signature) -> bool:            #метод принимает имя файла и подпись (хэш) далее вызываем __GenerateHash 
        if self.__GenerateHash(file) == decode(signature, self.secret_key, self.mod):#для получения хэша содержимого файла 
            print("Файл подтвержнен")                         #и сравнивает его с декодированной подписью, с помощью функции decode
            return True
        print("Файл не подтвержден")
        return False


if __name__ == "__main__":
    eds = EDS()                                        #Создается экземпляр класса EDS
    signature = eds.EncodeHash('2.txt')
    print(signature)
    eds.DecodeHash('1.txt', signature)