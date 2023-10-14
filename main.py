import re
import random

# region Глобальные переменные
ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"  # Стандартный алфавит
ALPHABET_VIGENERE = {
    "а": 1, "б": 2, "в": 3, "г": 4, "д": 5,
    "е": 6, "ё": 7, "ж": 8, "з": 9, "и": 10,
    "й": 11, "к": 12, "л": 13, "м": 14, "н": 15,
    "о": 16, "п": 17, "р": 18, "с": 19, "т": 20,
    "у": 21, "ф": 22, "х": 23, "ц": 24, "ч": 25,
    "ш": 26, "щ": 27, "ъ": 28, "ы": 29, "ь": 30,
    "э": 31, "ю": 32, "я": 33
}  # Алфавит для шифра Виженера

ALPHABET_POLYBIUS = {
    'а': 11, 'б': 12, 'в': 13, 'г': 14, 'д': 15, 'е': 16,
    'ё': 21, 'ж': 22, 'з': 23, 'и': 24, 'й': 25, 'к': 26,
    'л': 31, 'м': 32, 'н': 33, 'о': 34, 'п': 35, 'р': 36,
    'с': 41, 'т': 42, 'у': 43, 'ф': 44, 'х': 45, 'ц': 46,
    'ч': 51, 'ш': 52, 'щ': 53, 'ъ': 54, 'ы': 55, 'ь': 56,
    'э': 61, 'ю': 62, 'я': 63, '.': 64, ',': 65, '-': 66
}

STANDARD_SHIFT = 3
CHANGED_ALPHABET = {}  # Измененный алфавит


# endregion


def main():
    while True:
        input_text = input("Выберите действие для дальнейшего продолжения.\nДля выхода из программы напишите '0'. "
                           "Для шифрования напишите '1', для дешифрования '2': ")

        if input_text == '0':
            break
        elif input_text == '1':
            choice_of_method = input("Выберите метод шифрования:\n\tМетод ROTI с n сдвигом - '1'\n\tМетод ROTI с "
                                     "кодовым словом - '2'\n\tМетод квадрат Полибия - '3'\n\tМетод квадрат Полибия с "
                                     "кодовым словом - '4'\n\tМетод Виженера - '5'\n\tМетод Вернама - '6'\n\tВыход из "
                                     "меню - '0'\n")

            match choice_of_method.split():
                case ['1']: roti_n_shift(input_text)
                case ['2']: roti_code_word(input_text)
                case ['3']: polybius_square(input_text)
                case ['4']: polybius_square_code_word(input_text)
                case ['5']: vigenere(input_text)
                case ['6']: vernam(input_text)

        elif input_text == '2':
            choice_of_method = input("Выберите метод дешифрования:\n\tМетод ROTI с n сдвигом - '1'\n\tМетод ROTI с "
                                     "кодовым словом - '2'\n\tМетод квадрат Полибия - '3'\n\tМетод квадрат Полибия с "
                                     "кодовым словом - '4'\n\tМетод Виженера - '5'\n\tМетод Вернама - '6'\n\tВыход из "
                                     "меню - '0'\n")

            match choice_of_method.split():
                case ['1']: roti_n_shift(input_text)
                case ['2']: roti_code_word(input_text)
                case ['3']: polybius_square(input_text)
                case ['4']: polybius_square_code_word(input_text)
                case ['5']: vigenere(input_text)
                case ['6']: vernam(input_text)
        else:
            print("Введены некорректные данные!")


# region Метод ROTI с n сдвигом
def roti_n_shift(flag):
    encrypt_word = ""
    decrypt_word = ""
    if flag == "1":
        word = input("Введите шифруемое слово: ").lower()
        shift = int(input("Введите сдвиг: "))
        for letter in word:
            letter_index = ALPHABET.index(letter) + shift
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference
            encrypt_word += ALPHABET[letter_index]
        print("Зашифрованное слово: ", encrypt_word)
    elif flag == "2":
        word = input("Введите зашифрованное слово: ").lower()
        shift = int(input("Введите использованный сдвиг: "))
        for letter in word:
            letter_index = ALPHABET.index(letter) - shift
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference
            decrypt_word += ALPHABET[letter_index]
        print(decrypt_word)
# endregion+


# region ROTI с кодовым словом
def roti_code_word(flag):
    encrypt_word = ""
    decrypt_word = ""
    if flag == '1':
        word = input("Введите слово: ").lower()
        code_word = input("Введите кодовое слово, состоящее из уникальных букв: ").lower()
        for letter in code_word:
            if code_word.count(letter) > 1:
                print("Кодовое слово не содержит уникальных букв!")
                break

        local_alphabet = change_alphabet(code_word)

        for letter in word:
            letter_index = local_alphabet.index(letter) + STANDARD_SHIFT
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference
            encrypt_word += local_alphabet[letter_index]

        print(encrypt_word)
    elif flag == '2':
        word = input("Введите зашифрованное слово: ").lower()
        code_word = input("Введите кодовое слово, состоящее из уникальных букв: ").lower()
        for letter in code_word:
            if code_word.count(letter) > 1:
                print("Кодовое слово не содержит уникальных букв!")
                break

        local_alphabet = change_alphabet(code_word)

        for letter in word:
            letter_index = local_alphabet.index(letter) - STANDARD_SHIFT
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference
            decrypt_word += local_alphabet[letter_index]
        print(decrypt_word)
# endregion


def change_alphabet(code_word):
    local_alphabet = ALPHABET
    for letter in code_word:
        local_alphabet = local_alphabet.replace(letter, '')
    local_alphabet = code_word + local_alphabet
    return local_alphabet


# region Квадрат Полибия
def polybius_square(flag):
    encrypt_word = ""
    decrypt_word = ""
    if flag == '1':
        word = input("Введите слово: ").lower()
        shift = int(input("Введите сдвиг: "))
        for letter in word:
            index = ALPHABET_POLYBIUS[letter]
            index = shift_index(index, shift, True)
            encrypt_word += str(index)
        print(encrypt_word)

    elif flag == '2':
        word = input("Введите шифр: ").lower()
        shift = int(input("Введите сдвиг: "))
        number = ''
        for letter in word:
            number += letter
            if len(number) == 2:
                index = int(number)
                index = shift_index(index, shift, False)
                decrypt_word += get_key(index)
                number = ''
        print(decrypt_word)
# endregion


def get_key(index):
    for key, value in ALPHABET_POLYBIUS.items():
        if index == value:
            return key


def shift_index(index, shift, is_encrypt):
    if shift < 0:
        shift = shift.__abs__()

    count = 0
    if is_encrypt:
        while count < shift:
            if index == 16 or index == 26 or index == 36 or index == 46 or index == 56:
                index += 5
            elif index == 66:
                index = 11
            else:
                index += 1
            count += 1
    else:
        while count < shift:
            if index == 21 or index == 31 or index == 41 or index == 51 or index == 61:
                index -= 5
            elif index == 11:
                index = 66
            else:
                index -= 1
            count += 1
    return index


# region Квадрат Полибия с кодовым словом
def polybius_square_code_word(flag):
    encrypt_word = ''
    decrypt_word = ''
    number = ''
    if flag == '1':
        word = input("Введите слово: ").lower()
        code_word = input("Введите кодовое слово, состоящее из уникальных букв: ").lower()
        for letter in code_word:
            if code_word.count(letter) > 1:
                print("Кодовое слово не содержит уникальных букв!")
                break

        replace_code(code_word)

        for letter in word:
            number = int(CHANGED_ALPHABET[letter])
            encrypt_word += str(number)
        print(encrypt_word)

    if flag == '2':
        word = input("Введите зашифрованное слово: ").lower()
        code_word = input("Введите кодовое слово: ").lower()
        for letter in code_word:
            if code_word.count(letter) > 1:
                print("Кодовое слово не содержит уникальных букв!")
                break

        replace_code(code_word)

        for letter in word:
            number += letter
            if len(number) == 2:
                local_number = int(number)
                for key, value in CHANGED_ALPHABET.items():
                    if value == local_number:
                        decrypt_word += key
                number = ''
        print(decrypt_word)
# endregion


def replace_code(code_word):
    CHANGED_ALPHABET.clear()
    index_value = 11
    number_of_repetitions = 0
    for letter in code_word:
        CHANGED_ALPHABET[letter] = index_value
        index_value = validation_iterating_index_value(index_value)
    for base_key, base_value in ALPHABET_POLYBIUS.items():
        for local_key, local_value in CHANGED_ALPHABET.items():
            if base_key == local_key:
                number_of_repetitions += 1
        if number_of_repetitions == 0:
            CHANGED_ALPHABET[base_key] = index_value
            index_value = validation_iterating_index_value(index_value)
        number_of_repetitions = 0


def validation_iterating_index_value(number):
    if number == 16 or number == 26 or number == 36 or number == 46 or number == 56:
        number += 5
    else:
        number += 1
    return number


# region Метод Виженера
def vigenere(flag):
    decrypt_word = ''
    encrypt_word = ''
    letter_indices = []
    shifts = []
    if flag == '1':
        word = input("Введите слово: ").lower()
        code_word = input("Введите кодовое слово: ").lower()

        if len(code_word) < len(word):
            index = 0
            while len(code_word) < len(word):
                code_word += code_word[index]
                index += 1
        if len(code_word) > len(word):
            difference = len(code_word) - len(word)
            code_word = code_word[:-difference]

        for letter_in_word in word:
            letter_indices.append(ALPHABET.index(letter_in_word))
        for letter_in_code_word in code_word:
            for key, value in ALPHABET_VIGENERE.items():
                if letter_in_code_word == key:
                    shifts.append(value)

        for index in range(0, len(letter_indices)):
            letter_indices[index] += shifts[index]
            while letter_indices[index] > 32:
                difference = letter_indices[index] - 33
                letter_indices[index] = 0
                letter_indices[index] += difference
            encrypt_word += ALPHABET[letter_indices[index]]
        print(encrypt_word)

    elif flag == '2':
        word = input("Введите зашифрованное слово: ").lower()
        code_word = input("Введите кодовое слово: ").lower()

        if len(code_word) < len(word):
            index = 0
            while len(code_word) < len(word):
                code_word += code_word[index]
                index += 1
        if len(code_word) > len(word):
            difference = len(code_word) - len(word)
            code_word = code_word[:-difference]

        for letter_in_word in word:
            letter_indices.append(ALPHABET.index(letter_in_word))
        for letter_in_code_word in code_word:
            for key, value in ALPHABET_VIGENERE.items():
                if letter_in_code_word == key:
                    shifts.append(value)

        for index in range(0, len(letter_indices)):
            letter_indices[index] -= shifts[index]
            while letter_indices[index] < 0:
                difference = letter_indices[index] + 33
                letter_indices[index] = 0
                letter_indices[index] += difference
            decrypt_word += ALPHABET[letter_indices[index]]
        print(decrypt_word)
# endregion


def has_cyrillic(word):
    for letter in word:
        if ALPHABET.find(letter) == -1:
            return False
    return True


# region Метод Вермана
def vernam(flag):
    encrypt_word = ''
    decrypt_word = ''
    if flag == '1':
        word = input("Введите слово: ").lower()
        code_crypt = []
        code_crypt_index = 0
        for i in range(0, len(word)):
            code_crypt.append(random.randint(0, 33))
        for letter in word:
            letter_index = ALPHABET.index(letter)
            letter_index += code_crypt[code_crypt_index]
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference
            encrypt_word += ALPHABET[letter_index]
            code_crypt_index += 1
        print("Зашифрованное слово: ", encrypt_word)
        print("Шифр: ", code_crypt)

    elif flag == '2':
        word = input("Введите зашифрованное слово: ").lower()
        code_word = input("Введите шифр: ").lower()

        code_crypt_index = 0
        code_crypt = re.split(r"[ \[,\]]+", code_word)
        code_crypt.pop(0)
        code_crypt.pop(len(code_crypt) - 1)
        for letter in word:
            letter_index = ALPHABET.index(letter)
            letter_index -= int(code_crypt[code_crypt_index])
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference
            decrypt_word += ALPHABET[letter_index]
            code_crypt_index += 1
        print(decrypt_word)
# endregion


if __name__ == "__main__":
    main()
