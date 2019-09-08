from sys import argv


def main():
    # check args
    if len(argv) != 2:
        print('Usage: python bleep.py banned.txt')
        exit(1)

    # get input and split it
    print('What message would you like to censor?')
    in_text = input()
    words = in_text.split()

    # open and read file
    banned_file = open(argv[1], 'r')
    banned_words = banned_file.read()
    banned_words = banned_words.splitlines()

    match = False

    # iterate through every word in input
    for i in words:
        low_word = i.lower()
        # iterate through every banned word
        for j in banned_words:
            if low_word == j:
                print('*' * len(i), end=' ')
                match = True
        if match == False:
            print(i, end=' ')
        match = False
    print()


if __name__ == "__main__":
    main()
