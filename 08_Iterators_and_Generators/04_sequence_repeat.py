class sequence_repeat:
    def __init__(self, sequence, number):
        self.sequence = sequence
        self.number = number
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.number:
            i = self.i % len(self.sequence)
            self.i += 1
            return self.sequence[i]
        else:
            raise StopIteration




result = sequence_repeat('abc', 5)
for item in result:
    print(item, end='')
