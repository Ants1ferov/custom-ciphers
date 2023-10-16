import re
import random

# region Строки локализации
RES_MENU_SELECTION = ("Выберите действие для дальнейшего продолжения:\n\tШифрование - '1'\n\tДешифрование - "
                      "'2'\n\tВыход из программы - '0'\n--> ")
RES_CHOICE_OF_METHOD = ("\nВыберите метод:\n\tМетод ROTI с n сдвигом - '1'\n\tМетод ROTI с кодовым словом - "
                        "'2'\n\tМетод квадрат Полибия - '3'\n\tМетод квадрат Полибия с кодовым словом - '4'\n\tМетод "
                        "Виженера - '5'\n\tМетод Вернама - '6'\n\tВыход из меню - '0'\n--> ")
RES_INPUT_WORD = ["Введите шифруемое слово: ", "Введите зашифрованное слово: "]
RES_INPUT_SHIFT = ["Введите сдвиг: ", "Введите использованный сдвиг: "]
RES_GLOBAL_WORDS_RESULT = ["Зашифрованное слово: ", "Дешифрованное слово: "]
RES_INPUT_UNIQUE_CODE_WORD = "Введите кодовое слово, состоящее из уникальных букв: "
RES_INPUT_CODE_WORD = "Введите кодовое слово: "
# endregion


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


# region Точка входа
def main():
    while True:
        menu_selection = input(RES_MENU_SELECTION)

        match menu_selection.split():
            case ["0"]:
                break
            case ["1"] | ["2"]:
                choice_of_method = input(RES_CHOICE_OF_METHOD)
                match choice_of_method.split():
                    case ['1']:
                        roti_n_shift(menu_selection)
                    case ['2']:
                        roti_code_word(menu_selection)
                    case ['3']:
                        polybius_square(menu_selection)
                    case ['4']:
                        polybius_square_code_word(menu_selection)
                    case ['5']:
                        vigenere(menu_selection)
                    case ['6']:
                        vernam(menu_selection)
            case _:
                print("Введены некорректные символы!")
# endregion


# region Метод ROTI с n сдвигом (рефакторинг проведен)
def roti_n_shift(flag):
    result = ""

    word = input(RES_INPUT_WORD[int(flag) - 1]).lower()
    shift = int(input(RES_INPUT_SHIFT[int(flag) - 1]))

    for letter in word:

        letter_index = ALPHABET.index(letter)

        if flag == "1":
            letter_index += shift
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference

        elif flag == "2":
            letter_index -= shift
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference

        result += ALPHABET[letter_index]

    print(RES_GLOBAL_WORDS_RESULT[int(flag) - 1], result)
# endregion


# region ROTI с кодовым словом (рефакторинг проведен)
def roti_code_word(flag):
    result = ""

    word = input(RES_INPUT_WORD[int(flag) - 1]).lower()
    code_word = input(RES_INPUT_UNIQUE_CODE_WORD).lower()

    for letter in code_word:
        if code_word.count(letter) > 1:
            print("Кодовое слово не содержит уникальных букв!")
            break

    local_alphabet = ALPHABET
    for letter in code_word:
        local_alphabet = local_alphabet.replace(letter, '')
    local_alphabet = code_word + local_alphabet

    for letter in word:

        letter_index = local_alphabet.index(letter)

        if flag == '1':
            letter_index += STANDARD_SHIFT
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference

        elif flag == '2':
            letter_index -= STANDARD_SHIFT
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference

        result += local_alphabet[letter_index]

        print(RES_GLOBAL_WORDS_RESULT[int(flag) - 1], result)
# endregion


# region Квадрат Полибия (рефакторинг проведен)
def polybius_square(flag):
    result = ""
    number = ""

    word = input(RES_INPUT_WORD).lower()
    shift = int(input(RES_INPUT_SHIFT))

    for letter in word:
        if flag == '1':
            index = ALPHABET_POLYBIUS[letter]
            index = shift_index(index, shift, True)
            result += str(index)

        elif flag == '2':
            number += letter
            if len(number) == 2:
                index = int(number)
                index = shift_index(index, shift, False)
                for key, value in ALPHABET_POLYBIUS.items():
                    if index == value:
                        result += key
                number = ''

        print(RES_GLOBAL_WORDS_RESULT[int(flag) - 1], result)
# endregion


# region Квадрат Полибия с кодовым словом (рефакторинг проведен)
def polybius_square_code_word(flag):
    result = ""
    number = ""

    word = input(RES_INPUT_WORD).lower()
    code_word = input(RES_INPUT_UNIQUE_CODE_WORD).lower()

    for letter in code_word:
        if code_word.count(letter) > 1:
            print("Кодовое слово не содержит уникальных букв!")
            break

    CHANGED_ALPHABET.clear()
    index_value = 11
    number_of_repetitions = 0

    for letter in code_word:
        CHANGED_ALPHABET[letter] = index_value
        index_value = shift_index(index_value, 1, True)

    for base_key, base_value in ALPHABET_POLYBIUS.items():
        for local_key, local_value in CHANGED_ALPHABET.items():
            if base_key == local_key:
                number_of_repetitions += 1
        if number_of_repetitions == 0:
            CHANGED_ALPHABET[base_key] = index_value
            index_value = shift_index(index_value, 1, True)
        number_of_repetitions = 0

    for letter in word:
        if flag == '1':
            number = int(CHANGED_ALPHABET[letter])
            result += str(number)

        elif flag == '2':
            number += letter
            if len(number) == 2:
                local_number = int(number)
                for key, value in CHANGED_ALPHABET.items():
                    if value == local_number:
                        result += key
                number = ''

        print(RES_GLOBAL_WORDS_RESULT, result)
# endregion


# region Метод Виженера (рефакторинг проведен)
def vigenere(flag):
    letter_indices = []
    shifts = []
    result = ""

    word = input(RES_INPUT_WORD).lower()
    code_word = input(RES_INPUT_CODE_WORD).lower()

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
        if flag == '1':
            letter_indices[index] += shifts[index]
            while letter_indices[index] > 32:
                difference = letter_indices[index] - 33
                letter_indices[index] = 0
                letter_indices[index] += difference

        elif flag == '2':
            letter_indices[index] -= shifts[index]
            while letter_indices[index] < 0:
                difference = letter_indices[index] + 33
                letter_indices[index] = 0
                letter_indices[index] += difference

        result += ALPHABET[letter_indices[index]]

        print(RES_GLOBAL_WORDS_RESULT, result)
# endregion


# region Метод Вернама (рефакторинг проведен)
def vernam(flag):
    result = ""
    code_crypt = []
    code_crypt_index = 0

    word = input(RES_INPUT_WORD).lower()

    if flag == '1':
        for i in range(0, len(word)):
            code_crypt.append(random.randint(0, 33))
    elif flag == '2':
        code_word = input("Введите шифр: ").lower()
        code_crypt = re.split(r"[ \[,\]]+", code_word)
        code_crypt.pop(0)
        code_crypt.pop(len(code_crypt) - 1)

    for letter in word:

        letter_index = ALPHABET.index(letter)

        if flag == '1':
            letter_index += code_crypt[code_crypt_index]
            while letter_index > 32:
                difference = letter_index - 33
                letter_index = 0
                letter_index += difference

        elif flag == '2':
            letter_index -= int(code_crypt[code_crypt_index])
            while letter_index < 0:
                difference = letter_index + 33
                letter_index = 0
                letter_index += difference

        result += ALPHABET[letter_index]
        code_crypt_index += 1

    print(RES_GLOBAL_WORDS_RESULT, result)

    if flag == '2':
        print("Шифр: ", code_crypt)
# endregion


# region Дополнительные функции
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


def has_cyrillic(word):
    for letter in word:
        if ALPHABET.find(letter) == -1:
            return False
    return True
# endregion


if __name__ == "__main__":
    main()
