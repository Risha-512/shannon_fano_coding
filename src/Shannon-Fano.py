import sys

alphabet = []


def input_alphabet():
    try:
        with open("data/alphabet.txt") as fin:
            i = 0
            for line in fin:
                alphabet.append([''] * 3)
                data = line.split(' ')
                alphabet[i][0] = data[0]
                alphabet[i][1] = float(data[1])
                i += 1
        alphabet.sort(key=lambda x: x[1], reverse=True)
    except IOError:
        print("Error opening file 'alphabet.txt'")


def input_string():
    try:
        with open("data/string.txt") as fin:
            enc_str = fin.read()
            return enc_str
    except IOError:
        print("Error opening file 'string.txt'")


def input_code_str():
    try:
        with open("data/code_str.txt") as fin:
            code_str = fin.read()
            return code_str
    except IOError:
        print("Error opening file 'code_str.txt'")


def separator(begin, end):
    sum_full = 0
    for i in range(begin, end + 1):
        sum_full += alphabet[i][1]

    sum_l = 0
    sum_r = 0
    ind_l = begin
    ind_r = end

    while sum_l + sum_r < sum_full:
        if sum_l > sum_r:
            sum_r += alphabet[ind_r][1]
            ind_r -= 1
        else:
            sum_l += alphabet[ind_l][1]
            ind_l += 1

    for i in range(begin, ind_r + 1):
        alphabet[i][2] += '1'
    for i in range(ind_l, end + 1):
        alphabet[i][2] += '0'

    return ind_r


def create_code(ind_l, ind_r):
    if ind_l != ind_r:
        ind = separator(ind_l, ind_r)
        create_code(ind_l, ind)
        create_code(ind + 1, ind_r)


def searching_code(symb):
    for i in range(0, len(alphabet)):
        if alphabet[i][0] == symb:
            return alphabet[i][2]
    return '-'


def encoding(enc_str):
    res = ''
    for symb in enc_str:
        temp = searching_code(symb)
        if temp != '-':
            res += temp
        else:
            print("String can't be encoded")
            res = ''
            break
    return res


def decoding(code_str):
    res = ''
    while len(code_str) > 0:
        for i in range(0, len(alphabet)):
            if code_str.startswith(alphabet[i][2]):
                res += alphabet[i][0]
                temp_str = ''
                for j in range(len(alphabet[i][2]), len(code_str)):
                    temp_str += code_str[j]
                code_str = temp_str
        if res == '':               # not quite right condition => need to fix
            print("Code string can't be decoded")
            break
    return res


input_alphabet()
create_code(0, len(alphabet) - 1)
print(alphabet)
string = input_string()
print(string)
result = encoding(string)
print(result)
code_string = input_code_str()
print(code_string)
result = decoding(code_string)
print(result)
