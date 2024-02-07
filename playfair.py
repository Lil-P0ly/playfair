import collections
import random
import math
import copy


# Функция формирования ключа - матрицы
def matrix(key):
    matrix = []
    for e in key.upper():
        if e not in matrix:
            matrix.append(e)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for e in alphabet:
        if e not in matrix:
            matrix.append(e)

    # initialize a new list. Is there any elegant way to do that?
    matrix_group = []
    for e in range(5):
        matrix_group.append('')

    # Break it into 5*5
    matrix_group[0] = matrix[0:5]
    matrix_group[1] = matrix[5:10]
    matrix_group[2] = matrix[10:15]
    matrix_group[3] = matrix[15:20]
    matrix_group[4] = matrix[20:25]
    return matrix_group

# преобразование текста в биграммам для шифрования


def message_to_digraphs(message_original):
    # Change it to Array. Because I want used insert() method
    message = []
    print("Start Bigrams")
    # for e in message_original:
    #     message.append(e)

    # # Delet space
    # for unused in range(len(message)):
    #     if " " in message:
    #         message.remove(" ")
    message = list(message_original)
    # If both letters are the same, add an "X" after the first letter.
    i = 0
    half_len = int(len(message)/2)
    for e in range(half_len):
        if message[i] == message[i+1]:
            message.insert(i+1, 'X')
        i = i+2

    # If it is odd digit, add an "X" at the end
    if len(message) % 2 == 1:
        message.append("X")
    # Grouping
    i = 0
    new = []
    for x in range(1, int(len(message)/2)+1):
        new.append(message[i:i+2])
        i = i+2
  #  print("------- BIGRAMS ARE DONE -----------------")
    return new


def find_position(key_matrix, letter):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:
                x = i
                y = j

    return x, y


# функция зашифровывания
def encrypt(message, key_matrix):
    message = message_to_digraphs(message)
    # key_matrix = matrix(key)
    cipher = []
    for e in message:
        p1, q1 = find_position(key_matrix, e[0])
        p2, q2 = find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            cipher.append(key_matrix[p1][q1+1])
            cipher.append(key_matrix[p1][q2+1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            cipher.append(key_matrix[p1+1][q1])
            cipher.append(key_matrix[p2+1][q2])
        else:
            cipher.append(key_matrix[p1][q2])
            cipher.append(key_matrix[p2][q1])
    return cipher


def cipher_to_digraphs(cipher):
    i = 0
    new = []
    for x in range(int(len(cipher)/2)):
        new.append(cipher[i:i+2])
        i = i+2
    return new


def decrypt(cipher, key_matrix):
  #  print("----- STAGE 0 ---------")
    cipher = cipher_to_digraphs(cipher)
    # key_matrix = matrix(key)
    plaintext = []

 #   print("----- STAGE 1 ---------")

    for e in cipher:
        p1, q1 = find_position(key_matrix, e[0])
        p2, q2 = find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            plaintext.append(key_matrix[p1][q1-1])
            plaintext.append(key_matrix[p1][q2-1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            plaintext.append(key_matrix[p1-1][q1])
            plaintext.append(key_matrix[p2-1][q2])
        else:
            plaintext.append(key_matrix[p1][q2])
            plaintext.append(key_matrix[p2][q1])

 #  print("----- STAGE 2 ---------")

    # for unused in range(len(plaintext)):
    #     if "X" in plaintext:
    #         plaintext.remove("X")

    # plaintext = plaintext.replace('X', "")
    output = ""
    for e in plaintext:
        if "X" in e:
            e = e.replace('X', "")
        output += e
    return output

# не используем


def freq(string):
    letters_cr = dict(collections.Counter(string))
    # print(letters_cr)
    alphabet = letters_cr.keys()
    summa = 0
    for ltr in alphabet:
        summa += letters_cr[ltr]
    # print(summa)
    for ltr in alphabet:
        letters_cr[ltr] = letters_cr[ltr] / summa
    # print(letters_cr)
    return letters_cr


# не используем
def hi(basic_fr, this_fr):
    alphabet = this_fr.keys()
    val = 0
    for letter in alphabet:
        val += math.log10(basic_fr[letter] * this_fr[letter])
    return val

# не используем


def Prob(hi_old, hi_new, temperature):
    # print(hi_old, hi_new, temperature)
   # math.exp(-(hi_old - hi_new) / temperature)
    probs = math.exp((hi_new - hi_old) / temperature)
    # print("probs = ", probs)
    return probs


def swap_columns(matrix, col1=random.randint(0, 4), col2=random.randint(0, 4)):
    key_mtrx = copy.deepcopy(matrix)
    for row in matrix:
        row[col1], row[col2] = row[col2], row[col1]
    return key_mtrx


def swap_rows(matrix, row1=random.randint(0, 4), row2=random.randint(0, 4)):
    key_mtrx = copy.deepcopy(matrix)
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return key_mtrx


def reverse_rows(matrix):
    key_mtrx = copy.deepcopy(matrix)
    for row in key_mtrx:
        row.reverse()
    return key_mtrx


def reverse_columns(key_mtrx):
    matrix = copy.deepcopy(key_mtrx)

    num_rows = len(matrix)
    num_cols = len(matrix[0]) if matrix else 0

    for col in range(num_cols):
        column_values = [matrix[row][col] for row in range(num_rows)]
        column_values.reverse()

        for row in range(num_rows):
            matrix[row][col] = column_values[row]

    return matrix


def reverse_matrix(key_mtrx):
    matrix = copy.deepcopy(key_mtrx)

    # Переворачиваем строки матрицы
    matrix.reverse()

    # Переворачиваем значения в каждой строки матрицы
    for row in matrix:
        row.reverse()
    return matrix


def print_matrix(matrix):
    for row in matrix:
        for item in row:
            print(item, end='\t')
        print()


def change_key(mtrx_key):

    key_mtrx = copy.deepcopy(mtrx_key)

    x1 = random.randint(0, 4)
    y1 = random.randint(0, 4)

    x2 = random.randint(0, 4)
    y2 = random.randint(0, 4)

    while (x1 == x2 and y1 == y2):
        x2 = random.randint(0, 4)
        y2 = random.randint(0, 4)
    tmp = key_mtrx[x1][y1]
    key_mtrx[x1][y1] = key_mtrx[x2][y2]
    key_mtrx[x2][y2] = tmp

    return key_mtrx

# функция для оценки текста


def function_quality(d_quadrams, text, total_sum):
    qual_mark = 0
    for i in range(0, len(text)-3):
        # print(text[i:i+4])
        if text[i:i+4] in d_quadrams:
            k_vak = math.log10(d_quadrams[text[i:i+4]] / total_sum)
        else:
            k_vak = math.log10(1 / total_sum)
        # print("log10 = ", k_vak)
        qual_mark += k_vak
    return qual_mark


# key="cipher"
# message="effecttreecorrectapple"
# cipher="FNNFHOODPZCIVGFCHOBIBSPZ"


# message = "Hide the gold in the tree stump"
# >>BMODZBXDNABEKUDMUIXMMOUVIF
# print(matrix(key))

f = open("book1.txt", 'r')
text = f.read()
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())
first_text = out_text
letters = dict(collections.Counter(out_text))
key = "password"
matrix_key = matrix(key)

print_matrix(matrix_key)


# selected_function = random.choices([change_key, swap_columns, swap_rows, reverse_rows,
#                                    reverse_columns, reverse_matrix], weights=[90, 2, 2, 2, 2, 2], k=1)[0]
# matrix_key_1 = selected_function(matrix_key)
# print_matrix(matrix_key_1)

# print("-------------------")
# # matrix_key_1 = swap_columns(matrix_key, 0, 4)
# matrix_key_1 = reverse_matrix(matrix_key)
# print_matrix(matrix_key_1)
# print("-------------------")
# print_matrix(matrix_key)


# basic_freq = freq(letters)
# print("basic_frec = ")
# print(basic_freq)

# basic_hi = hi(basic_freq, basic_freq)
# print("basic_hi = ")
# print(basic_hi)

f.close()

text = str(encrypt(out_text, matrix_key))
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())

f = open("playfair.txt", 'w')
f.write(out_text)
f.close()


# пытаемся расшифровать матрицу рандномным ключом

key_rand = 'rfclkj'
matrix_key_rand = matrix(key_rand)

f = open("playfair.txt", 'r')
text = f.read()
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())

# print(out_text[0:50])
dc_tx = decrypt(out_text, matrix_key_rand)
# old_freq = freq(dc_tx)
# old_hi = hi(basic_freq, old_freq)
# print(dt[0:50])
f.close()


d_quadrams = {}
total_sum = 0
with open("4grams.txt") as f:
    for line in f:
        (key, val) = line.split()
        d_quadrams[key] = int(val)
        total_sum += int(val)

# test = "HAPPYDAYSNZQZ"
# mrks = function_quality(d_quadrams, test)
# print(mrks)


T_0 = 1

best_hi = -10000000000000000
best_text = ""

old_hi = function_quality(d_quadrams, dc_tx, total_sum)
while T_0 >= 1:

    for i in range(0, 50000):

        # iter_matrix_key_rand = change_key(matrix_key_rand)

        # мы должны рандомно выбрать способ изменения
        selected_function = random.choices([change_key, swap_columns, swap_rows, reverse_rows,
                                            reverse_columns, reverse_matrix], weights=[90, 2, 2, 2, 2, 2], k=1)[0]
        iter_matrix_key_rand = selected_function(matrix_key_rand)

        dc_tx = decrypt(out_text, iter_matrix_key_rand)
        new_hi = function_quality(d_quadrams, dc_tx, total_sum)
        dF = new_hi - old_hi
        # print("new = ", new_hi, "old = ", old_hi)
        # print("dF = ", dF)
        if dF > 0:
            old_hi = new_hi
            matrix_key_rand = copy.deepcopy(iter_matrix_key_rand)
        else:
            prob_iter = math.exp(dF / T_0)

           # print("prob_iter = ", prob_iter, "dF = ", dF)
            if prob_iter > random.random():
                old_hi = new_hi
                matrix_key_rand = copy.deepcopy(iter_matrix_key_rand)
              #  print("DOWN")
        # new_freq = freq(dc_tx)
        # new_hi = hi(basic_freq, new_freq)

        if old_hi > best_hi:
            best_hi = old_hi
            best_text = dc_tx
            best_key = copy.deepcopy(matrix_key_rand)
            print("NEW BEST = ", best_hi)

        # if new_hi > old_hi:
        #     old_hi = new_hi
        #     matrix_key_rand = iter_matrix_key_rand
        #     print(old_hi)
        # if new_hi < old_hi:
        #     random_number = random.random()

        #     if random_number < Prob(old_hi, new_hi, T_0):
        #         print("e = ", Prob(old_hi, new_hi, T_0))
        #         old_hi = new_hi
        #         matrix_key_rand = iter_matrix_key_rand

    T_0 = T_0 - 1
    print("T_0 = ", T_0)


# print(matrix_key)
# print(matrix_key_rand)

print(best_hi)
print(best_key)
print(first_text[0:50])
print(best_text[0:50])
# # print(old_hi)
