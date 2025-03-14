class DFF:
    def __init__(self):
        self.q = 0  # Estado inicial

    def update(self, d):
        self.q = d  # En hardware real, esto ocurre en un ciclo de reloj


class Bit:
    def __init__(self):
        self.dff = DFF()

    def update(self, input_bit, load):
        if load:
            self.dff.update(input_bit)
        return self.dff.q


class Register:
    def __init__(self):
        self.bits = [Bit() for _ in range(16)]

    def update(self, input_word, load):
        return [self.bits[i].update(input_word[i], load) for i in range(16)]


class RAMn:
    def __init__(self, n):
        self.size = n
        self.memory = [Register() for _ in range(n)]

    def update(self, input_word, address, load):
        output = [0] * 16
        for i in range(self.size):
            if i == address:
                output = self.memory[i].update(input_word, load)
            else:
                self.memory[i].update(self.memory[i].update([0]*16, 0), 0)
        return output
