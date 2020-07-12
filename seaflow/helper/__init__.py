def create_secret():
    import os
    return os.urandom(16)


if __name__ == '__main__':
    print(create_secret())
