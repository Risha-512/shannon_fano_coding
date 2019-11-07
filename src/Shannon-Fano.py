import csv
import sys

alphabet = []
input_string = ''


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
        print('Error opening' + path)


def read_line_from_file(path):
    try:
        with open(path) as fin:
            return fin.readline()
    except IOError:
        print('Error opening' + path)


def save_line_to_file(string, path):
    try:
        with open(path, 'w+') as fout:
            fout.write(string)
    except IOError:
        print('Error creating' + path)


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


def add_test_bit():
    for item in alphabet:
        bits_sum = 0
        for c in item[2]:
            bits_sum += int(c)
        item[2] += '0' if bits_sum % 2 == 0 else '1'


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
            print('String can\'t be encoded')
            return 'None'
    return res


def searching_symbol(code_str):
    for i in range(len(alphabet)):
        if code_str.startswith(alphabet[i][2]):
            return i
    return '-'


def hamming_distance(code):         # minimum distance between this code and code from alphabet
    distance = len(alphabet[0][2])
    for i in alphabet:
        if code != i[2]:
            cur_distance = sum(c1 != c2 for c1, c2 in zip(code, i[2]))
            if distance > cur_distance:
                distance = cur_distance
    return distance


def decode(code_str):
    res = ''
    errors_positions = []
    code_index = 0

    while len(code_str) > 0:
        i = searching_symbol(code_str)
        if i != '-':
            res += alphabet[i][0] + ' '
        else:
            errors_positions.append(str(code_index + 1) + ' - ' + str(code_index + len(alphabet[0][2])))
        code_str = code_str[len(alphabet[0][2]):]
        code_index += len(alphabet[0][2])
    return res, errors_positions if len(errors_positions) != 0 else 'No errors'


if __name__ == '__main__':
    # If script doesn't have 5 arguments then exit
    if len(sys.argv) != 5 or sys.argv[1] != 'e' and sys.argv[1] != 'd':
        print('(en|de)coding: Shannon-Fano.py [e|d] [path]Alphabet [path]Input_String [path]Output_String')
        sys.exit(1)

    # Read alphabet from file path provided in 2 argument
    read_alphabet_file(sys.argv[2])

    # Read input string from file path provided in 3 argument
    input_string = read_line_from_file(sys.argv[3])

    # Encode alphabet with Shannon-Fano algorithm and print it
    shannon_fano(0, len(alphabet) - 1)
    print('Alphabet without test bit:\n', alphabet, '\n')
    add_test_bit()
    print('Alphabet with test bit:\n', alphabet)
    print()

    # Count Hamming distances
    print('Distance:', hamming_distance(alphabet[0][2]))

    # Encode or Decode and store result
    if sys.argv[1] == 'e':
        print('Encoding: ' + input_string)
        result = encode(input_string)
    else:
        print('Decoding: ' + input_string)
        result, errors = decode(input_string)
        print('Errors positions:', errors)

    # Print result
    print('Result: ' + result)

    # Save result to file path provided in 4 argument
    save_line_to_file(result, sys.argv[4])
    print('Saved result to: ' + sys.argv[4])
