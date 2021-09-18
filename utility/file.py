class File:
    def __init__(self):
        return

    @staticmethod
    def open(path='/path/to/file'):
        with open(path, 'r') as f:
            file = f.read()
            return file

    def write(path='/path/to/file', string='Hello, world!'):
        with open(path, 'w') as f:
            f.write(string)



