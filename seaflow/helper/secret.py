from random import randint, choice


def create_secret():
    import os
    return os.urandom(16)


def create_check_code():
    return random_code(4)


def random_code(n=4, need_letter=True):
    s = ''
    for i in range(n):
        num = randint(0, 9)
        if need_letter:
            upper_letter = chr(randint(65, 90))
            lower_letter = chr(randint(97, 122))
            num = choice([num, upper_letter, lower_letter])
        s = s + str(num)
    return s


def create_salt():
    n = randint(4, 6)
    return random_code(n=n)


if __name__ == '__main__':
    print(create_secret())
