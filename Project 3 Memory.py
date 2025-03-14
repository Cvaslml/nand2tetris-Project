class DFF:
    """ Flip-Flop tipo D para almacenamiento de 1 bit """
    def __init__(self):
        self.state = 0

    def update(self, inp):
        self.state = inp
        return self.state


class Bit:
    """ Bit almacenable basado en DFF """
    def __init__(self):
        self.dff = DFF()

    def update(self, inp, load):
        if load:
            return self.dff.update(inp)
        return self.dff.state


class Register:
    """ Registro de 16 bits compuesto por 16 Bits """
    def __init__(self):
        self.bits = [Bit() for _ in range(16)]

    def update(self, input_word, load):
        return [self.bits[i].update(input_word[i], load) for i in range(16)]


class RAMn:
    """ Memoria RAM de tamaño n con acceso mediante PC """
    def __init__(self, size):
        self.size = size
        self.memory = [Register() for _ in range(size)]
        self.pc = PC()

    def update(self, address, input_word, load, inc, reset):
        """
        - address: Dirección de memoria a acceder.
        - input_word: Palabra de 16 bits a escribir.
        - load: Indica si se debe escribir en la dirección actual.
        - inc: Indica si el PC debe incrementarse automáticamente.
        - reset: Resetea el PC a 0.
        """
        pc_address = self.pc.update(address, 0, inc, reset)
        address_int = int("".join(map(str, pc_address)), 2) % self.size
        return self.memory[address_int].update(input_word, load)


class PC:
    """ Contador de Programa de 16 bits """
    def __init__(self):
        self.register = Register()

    def update(self, input_word, load, inc, reset):
        if reset:
            return self.register.update([0] * 16, 1)  # Reset a 0
        elif load:
            return self.register.update(input_word, 1)  # Cargar nuevo valor
        elif inc:
            return self.register.update(inc16(self.register.update([0] * 16, 0)), 1)  # Incrementar
        else:
            return self.register.update(self.register.update([0] * 16, 0), 0)  # Mantener valor


def inc16(a):
    """ Incrementador de 16 bits """
    b = [0] * 15 + [1]
    return add16(a, b)


def add16(a, b):
    """ Suma de 16 bits utilizando Full Adder """
    output = [0] * 16
    carry = 0
    for i in range(15, -1, -1):
        result = fulladder(a[i], b[i], carry)
        output[i] = result["Sum_F"]
        carry = result["Carry_F"]
    return output


def fulladder(a, b, c):
    """ Full Adder para suma de 3 bits """
    out1 = halfadder(a, b)
    sum_result = halfadder(out1["Sum_H"], c)
    carry = or_chip(out1["Carry_H"], sum_result["Carry_H"])
    return {"Carry_F": carry, "Sum_F": sum_result["Sum_H"]}


def halfadder(a, b):
    """ Half Adder para suma de 2 bits """
    sum_result = xor_chip(a, b)
    carry = and_chip(a, b)
    return {"Carry_H": carry, "Sum_H": sum_result}


def and_chip(a, b):
    """ AND con NAND """
    return nand(nand(a, b), nand(a, b))


def or_chip(a, b):
    """ OR con NAND """
    return nand(nand(a, a), nand(b, b))


def xor_chip(a, b):
    """ XOR con NAND """
    n1 = nand(a, b)
    n2 = nand(a, n1)
    n3 = nand(n1, b)
    return nand(n2, n3)


def nand(a, b):
    """ Compuerta NAND básica """
    return 0 if (a == 1 and b == 1) else 1


# 🛠️ Prueba de la RAMn con PC
ram = RAMn(8)  # 8 registros de 16 bits

# Escritura en la dirección 3
ram.update([0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 1, 0, 0)

# Incrementar PC y leer siguiente dirección
print(ram.update([0, 0, 0, 0, 0, 0, 0, 0], [0]*16, 0, 1, 0))

# Resetear el PC y leer nuevamente la primera dirección
print(ram.update([0, 0, 0, 0, 0, 0, 0, 0], [0]*16, 0, 0, 1))

