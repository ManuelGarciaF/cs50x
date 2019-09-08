from sys import argv, exit

UPPERCASE = 65
LOWERCASE = 97

def main():
    if len(argv) != 2:
        print('Usage: python vigenere.py key')
        exit(1)
    else:
        if not argv[1].isalpha():
            print('Usage: python vigenere.py key')
            exit(1)


    k_word = argv[1]
    k_len = len(k_word)
    p_text = input('plaintext: ')
    c_text = ""

    j = 0

    for i in p_text:
        p_val, is_up = get_num_value(i)
        k_val, _k_is_up = get_num_value(k_word[j])

        out = p_val + k_val
        if out > 25:
            out -= 26

        if is_up and p_val >= 0:
            out += UPPERCASE
        elif p_val >= 0:
            out += LOWERCASE
        else:
            out = ord(i)
        c_text += chr(out)

        if p_val >= 0:
           j += 1

        if j == k_len:
           j = 0

    print("ciphertext: " + c_text)


def get_num_value(i):
    if i.isupper():
        val = ord(i) - UPPERCASE
        return val, True
    elif i.islower():
        val = ord(i) - LOWERCASE
        return val, False
    else:
        return -1, False


if __name__ == '__main__':
    main()
