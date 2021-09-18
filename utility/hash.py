import hashlib


class HashHandler:
    def __init__(self, obj):
        self.obj = obj
        self.transform()

    def transform(self):
        if isinstance(self.obj, dict):
            self.md5 = self.gen_hash_dict(self.obj)
        if isinstance(self.obj, str):
            self.md5 = self.gen_hash_str(self.obj)
        if isinstance(self.obj, list):
            self.md5 = self.gen_hash_list(self.obj)

    @staticmethod
    def gen_hash_str(p_str):
        p_bytes = p_str.encode('utf-8')
        md5 = hashlib.md5(p_bytes).hexdigest()
        return md5

    def gen_hash_dict(self, p_dict):
        temp_list = [str(i) for i in p_dict.values()]
        temp_str = ''.join(temp_list)
        return self.gen_hash_str(temp_str)

    def gen_hash_list(self, p_list):
        temp_list = [str(i) for i in p_list]
        temp_str = ''.join(temp_list)
        return self.gen_hash_str(temp_str)


if __name__ == "__main__":
    d = {'a': 1, 'b': 2, 'c': '3'}
    s = "string"
    l = ['1', 2, 'hello']
    print(HashHandler(l).md5)
