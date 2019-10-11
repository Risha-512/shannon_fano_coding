import csv
import sys
import math


alphabet = []
input_string = ''


def read_alphabet_file(path):
    global alphabet
    try:
        with open(path) as csv_file:
            cvs_reader = csv.reader(csv_file, delimiter=' ')
            i = 0
            for row in cvs_reader:
                alphabet.append([''] * 3)
                alphabet[i][0] = row[0]
                alphabet[i][1] = float(row[1])
                alphabet[i][2] = ''
                i += 1
        alphabet.sort(key=lambda x: x[1], reverse=True)
    except IOError:
        print("Error opening" + path)


def read_line_from_file(path):
    try:
        with open(path) as fin:
            return fin.readline()
    except IOError:
        print("Error opening" + path)


def save_line_to_file(string, path):
    try:
        with open(path, 'w+') as fout:
            fout.write(string)
    except IOError:
        print("Error creating" + path)


def shannon_fano(start, end):
    global alphabet

    size = end - start + 1

    if size == 2:
        alphabet[start][2] += '1'
        alphabet[end][2] += '0'

    elif size > 1:
        sum_l = sum_r = 0
        ind_l = start
        ind_r = end
        while ind_l != ind_r:
            if sum_l > sum_r:
                sum_r += alphabet[ind_r][1]
                ind_r -= 1
            else:
                sum_l += alphabet[ind_l][1]
                ind_l += 1

        for index in range(start, end + 1):
            if index <= ind_l:
                alphabet[index][2] += '1'
            else:
                alphabet[index][2] += '0'

        shannon_fano(start, ind_l)
        shannon_fano(ind_l + 1, end)


def searching_code(symb):
    for i in range(0, len(alphabet)):
        if alphabet[i][0] == symb:
            return alphabet[i][2]
    return '-'


def encode(enc_str):
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


def decode(code_str):
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


def Kraft_inequality():
    vect = []
    for index in range(0, len(alphabet)):
        vect.append(len(alphabet[index][2]))
    print("Kraft's Vector: ", vect)
    inequality = 0
    for index in range(0, len(vect)):
        inequality += pow(2, -vect[index])
    print("Inequality: ", inequality)
    return inequality <= 1.0


def redundancy():
    entropy = 0
    max_entropy = math.log2(len(alphabet))
    for i in range(0, len(alphabet)):
        entropy -= alphabet[i][1] * math.log2(alphabet[i][1])
    return 1 - entropy/max_entropy


def generate_string(n, path):
    with open(path, "w") as file:
        for index in range(len(alphabet)):
            file.write(alphabet[index][0] * int(alphabet[index][1] * n))


if __name__ == '__main__':
    # If script doesn't have 5 arguments or first argument isn't e or d, then exit
    if len(sys.argv) != 5 or not (sys.argv[1] == 'e' or sys.argv[1] == 'd'):
        print("Usage: Shannon-Fano.py [e|d] [path]Alphabet file [path]Input String file [path]Output String file")
        sys.exit(1)

    # Read alphabet from file path provided in 2 argument
    read_alphabet_file(sys.argv[2])

    # Read input string from file path provided in 3 argument
    input_string = read_line_from_file(sys.argv[3])

    # Encode alphabet with Shannon-Fano algorithm and print it
    shannon_fano(0, len(alphabet) - 1)
    print(alphabet)
    print()

    # Check for Kraft's inequality
    print("Kraft's inequality is", Kraft_inequality())

    # Redundancy check
    print("Redundancy:", redundancy())
    print()

    # Encode or Decode and store result
    if sys.argv[1] == 'e':
        print("Encoding: " + input_string)
        result = encode(input_string)
    else:
        print("Decoding: " + input_string)
        result = decode(input_string)

    # Print result
    print("Result: " + result)

    # Save result to file path provided in 4 argument
    save_line_to_file(result, sys.argv[4])
    print("Saved result to: " + sys.argv[4])
