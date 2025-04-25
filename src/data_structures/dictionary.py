# Dictionary module

class twoWayDict():
    def __init__(self):
        self.dictionary = dict()

    def add(self, item_1, item_2):
        self.dictionary[item_1] = item_2
        self.dictionary[item_2] = item_1

    def delete(self, item):
        pair = self.dictionary[item]
        del self.dictionary[item]
        del self.dictionary[pair]

    def __len__(self):
        return len(self.dictionary) // 2

    def __getitem__(self, key):
        if key not in self.dictionary:
            raise KeyError(f'{key} was not found in twoWayDict.')
        return self.dictionary[key]
    
if __name__ == "__main__":
    d = twoWayDict()
    d.add(1, 2)
    d.add(3, 4)
    for i in range(1, 5):
        print(f'{i} -> {d[i]}')
    d.delete(1)
    v = d[1]