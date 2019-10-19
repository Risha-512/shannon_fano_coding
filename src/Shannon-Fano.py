import csv
import sys
import math
from collections import defaultdict

alphabet = []
input_string = ''
text = ''


def read_text(path):
    global text

    try:
        with open(path, 'r') as file:
            text = file.read().replace('\n', '').replace(" ", "").lower()
    except IOError:
        print("Error opening" + path)


def frequency_analysis():
    global alphabet

    frequencies = defaultdict(lambda: 0)

    for c in text:
        frequencies[c] += 1

    i = 0
    for item in frequencies:
        alphabet.append(['']*3)
        alphabet[i][0] = item
        alphabet[i][1] = frequencies[item] / len(frequencies)
        i += 1
    alphabet.sort(key=lambda x: x[1], reverse=True)


def read_alphabet_file(path):
    global alphabet
    try:
        with open(path) as csv_file:
            cvs_reader = csv.reader(csv_file, delimiter=' ')
            i = 0
            for row in cvs_reader:
                if float(row[1]) != 0.0:
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

        if sum_l < sum_r:
            ind_l += 1

        for index in range(start, end + 1):
            if index < ind_l:
                alphabet[index][2] += '1'
            else:
                alphabet[index][2] += '0'

        shannon_fano(start, ind_l - 1)
        shannon_fano(ind_l, end)


def searching_code(symb):
    for i in range(len(alphabet)):
        if alphabet[i][0] == symb:
            return alphabet[i][2]
    return '-'


def encode(enc_str):
    res = ''
    enc_str = enc_str.split(' ')
    enc_str = enc_str[:len(enc_str) - 1]  # Get rid of the last space
    for symb in enc_str:
        temp = searching_code(symb)
        if temp != '-':
            res += temp
        else:
            print("String can't be encoded")
            return 'None'
    return res


def searching_symbol(code_str):
    for i in range(len(alphabet)):
        if code_str.startswith(alphabet[i][2]):
            return i
    return '-'


def decode(code_str):
    res = ''
    while len(code_str) > 0:
        i = searching_symbol(code_str)
        if i != '-':
            res += alphabet[i][0] + ' '
            code_str = code_str[len(alphabet[i][2]):]
        else:
            print("Code string can't be decoded")
            return 'None'
    return res


def Kraft_inequality():
    vect = []
    for index in range(len(alphabet)):
        vect.append(len(alphabet[index][2]))
    print("Kraft's Vector: ", vect)
    inequality = 0
    for index in range(len(vect)):
        inequality += math.pow(2, -vect[index])
    print("Kraft's value: ", inequality)
    return inequality <= 1.0


def average_code_length():
    res = 0
    for i in range(len(alphabet)):
        res += alphabet[i][1] * len(alphabet[i][2])
    return res


def redundancy():
    entropy = 0
    for i in range(len(alphabet)):
        entropy -= alphabet[i][1] * math.log2(alphabet[i][1])
    return average_code_length() - entropy


def generate_string(n, path):
    with open(path, "w") as file:
        for index in range(len(alphabet)):
            file.write((alphabet[index][0] + ' ') * int(alphabet[index][1] * n))


if __name__ == '__main__':
    # If script doesn't have 5 arguments then exit
    if len(sys.argv) != 5 and sys.argv[1] != 's':
        print("(en|de)coding: Shannon-Fano.py [e|d] [path]Alphabet [path]Input_String [path]Output_String")
        print("Generate string: Shannon-Fano.py g [int]String_Length [path]Alphabet [path]Output_String")
        print("Static analysis: Shannon-Fano.py s [path]Text")
        sys.exit(1)

    # If first argument is 'g' then generate string from alphabet probability
    if sys.argv[1] == 'g':
        # Read alphabet from file path provided in 3 argument
        read_alphabet_file(sys.argv[3])

        # Generate string with length provided in 2 argument
        # to file path provided in 4 argument
        generate_string(int(sys.argv[2]), sys.argv[4])

        print("Creating string with ", sys.argv[2], "elements.")
        print("From " + sys.argv[3])
        print("To" + sys.argv[4])
        sys.exit()

    if sys.argv[1] == 's':
        # Read text from file
        read_text(sys.argv[2])
        # Perform frequency analysis
        frequency_analysis()

    if sys.argv[1] == 'e' or sys.argv[1] == 'd':
        # Read alphabet from file path provided in 2 argument
        read_alphabet_file(sys.argv[2])

        # Read input string from file path provided in 3 argument
        input_string = read_line_from_file(sys.argv[3])

    # Encode alphabet with Shannon-Fano algorithm and print it
    shannon_fano(0, len(alphabet) - 1)
    print("Alphabet:\n", alphabet)
    print()

    # Calculate and print average code length
    print("Average code length: ", average_code_length())
    print()

    # Calculate and print redundancy
    print("Redundancy:", redundancy())
    print()

    # Check for Kraft's inequality
    print("Kraft's inequality is", Kraft_inequality())
    print()

    # Encode or Decode and store result
    # if sys.argv[1] == 'e' or sys.argv[1] == 's':
    #     print("Encoding: " + input_string)
    #     result = encode(input_string)
    # else:
    #     print("Decoding: " + input_string)
    #     result = decode(input_string)
    #
    # # Print result
    # print("Result: " + result)
    #
    # # Save result to file path provided in 4 argument
    # save_line_to_file(result, sys.argv[4])
    # print("Saved result to: " + sys.argv[4])
