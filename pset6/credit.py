def main():
    while True:
        num = int(input('Number: '))
        if num > 0:
            break
    numlen = len(str(num))
    
    vernum = num
    for _ in range(numlen - 2):
        vernum //= 10
    # Check luhn
    if luhn(num) == False:
        print('INVALID')
    elif numlen == 15 and vernum == 34 or 37:
        print('AMEX')
    elif numlen == 16 and vernum >= 51 and vernum <= 55:
        print('MASTERCARD')
    elif numlen == 13 or 16 and (vernum // 10) == 4:
        print('VISA')
    else:
        print('INVALID')

def luhn(n):
    toggle = False
    total = 0
    for _ in range(len(str(n))):
        if toggle:
            tempA = (n % 10) * 2
            total += tempA // 10 + tempA % 10
        else:
            tempB = (n % 10)
            total += tempB
        toggle = not toggle
        n //= 10
    if total % 10 == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    main()