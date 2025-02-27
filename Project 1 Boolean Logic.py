#Primero hicimos la implementación de la compuerta primitiva para así armar todas 
#en base a esta, la modelamos como una función para usar recursividad en las otras.

def nand(a, b):
    """Comportamiento de una compuerta NAND."""
    return 0 if (a == 1 and b == 1) else 1


# 1. Compuerta NOT
def not_chip(a=1):
    out = nand(a, a)
    print(f"NOT({a}) -> {out}")
    return out


# 2. Compuerta AND
def and_chip(a=1, b=1):
    out = nand(nand(a, b), nand(a, b))
    print(f"AND({a}, {b}) -> {out}")
    return out


# 3. Compuerta OR
def or_chip(a=0, b=0):
    out = nand(nand(a, a), nand(b, b))
    print(f"OR({a}, {b}) -> {out}")
    return out


# 4. Compuerta XOR
def xor_chip(a=0, b=0):
    n1 = nand(a, b)
    n2 = nand(a, n1)
    n3 = nand(n1, b)
    out = nand(n2, n3)
    print(f"XOR({a}, {b}) -> {out}")
    return out


# 5. Compuerta MUX (Multiplexor)
def mux_chip(a=0, b=1, sel=0):
    n1 = nand(sel, sel)
    n2 = nand(b, sel)
    n3 = nand(a, n1)
    out = nand(n2, n3)
    print(f"MUX(A={a}, B={b}, SEL={sel}) -> {out}")
    return out


# 6. Compuerta DMUX (Demultiplexor)
def dmux_chip(a=1, sel=0):
    n1 = nand(sel, sel)
    n2 = nand(a, n1)
    n3 = nand(a, sel)
    out1 = nand(n2, n2)
    out2 = nand(n3, n3)
    print(f"DMUX(IN={a}, SEL={sel}) -> ({out1}, {out2})")
    return out1, out2


# 7. Compuerta NOT16
def not16_chip(a=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]):
    out = [nand(bit, bit) for bit in a]
    print(f"NOT16({a}) -> {out}")
    return out


# 8. Compuerta AND16
def and16_chip(
    a=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    b=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
):
    out = [nand(nand(a[i], b[i]), nand(a[i], b[i])) for i in range(16)]
    print(f"AND16(A={a}, B={b}) -> {out}")
    return out


# 9. Compuerta OR16
def or16_chip(
    a=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    b=[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
):
    out = [nand(nand(a[i], a[i]), nand(b[i], b[i])) for i in range(16)]
    print(f"OR16(A={a}, B={b}) -> {out}")
    return out


# 10. Compuerta MUX16
def mux16_chip(
    a=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    b=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    c=0,
):
    n1 = nand(c, c)
    out = [nand(nand(b[i], c), nand(a[i], n1)) for i in range(16)]
    print(f"MUX16(A={a}, B={b}, SEL={c}) -> {out}")
    return out


def nand(a, b):
    """Comportamiento de una compuerta NAND."""
    return 0 if (a == 1 and b == 1) else 1


# 11. Compuerta OR8Way
def or8way(a=[0, 0, 0, 0, 0, 0, 0, 1]):
    out = nand(nand(or_chip(a[0], a[1]), or_chip(a[2], a[3])),
               nand(or_chip(a[4], a[5]), or_chip(a[6], a[7])))
    print(f"OR8WAY({a}) -> {out}")
    return out


# 12. Compuerta MUX4Way16
def mux4way16(
    a=[1] * 16, b=[0] * 16, c=[1, 0] * 8, d=[0, 1] * 8, sel=[1, 0]
):
    mux1 = mux16_chip(a, b, sel[0])
    mux2 = mux16_chip(c, d, sel[0])
    out = mux16_chip(mux1, mux2, sel[1])
    print(f"MUX4WAY16(A={a}, B={b}, C={c}, D={d}, SEL={sel}) -> {out}")
    return out


# 13. Compuerta MUX8Way16
def mux8way16(
    a=[1] * 16, b=[0] * 16, c=[1, 0] * 8, d=[0, 1] * 8,
    e=[1, 1] * 8, f=[0, 0] * 8, g=[1, 1] * 8, h=[0, 0] * 8,
    sel=[1, 0, 1]
):
    mux1 = mux4way16(a, b, c, d, sel[:2])
    mux2 = mux4way16(e, f, g, h, sel[:2])
    out = mux16_chip(mux1, mux2, sel[2])
    print(f"MUX8WAY16(A={a}, ..., H={h}, SEL={sel}) -> {out}")
    return out


# 14. Compuerta DMUX4Way
def dmux4way(a=1, sel=[1, 0]):
    out1, out2 = dmux_chip(a, sel[1])
    o1, o2 = dmux_chip(out1, sel[0])
    o3, o4 = dmux_chip(out2, sel[0])
    print(f"DMUX4WAY(IN={a}, SEL={sel}) -> ({o1}, {o2}, {o3}, {o4})")
    return o1, o2, o3, o4


# 15. Compuerta DMUX8Way
def dmux8way(a=1, sel=[1, 0, 1]):
    out1, out2 = dmux_chip(a, sel[2])
    o1, o2, o3, o4 = dmux4way(out1, sel[:2])
    o5, o6, o7, o8 = dmux4way(out2, sel[:2])
    print(f"DMUX8WAY(IN={a}, SEL={sel}) -> ({o1}, {o2}, {o3}, {o4}, {o5}, {o6}, {o7}, {o8})")
    return o1, o2, o3, o4, o5, o6, o7, o8

def mostrar_menu():
    print("\n=== MENÚ DE COMPUESTAS LÓGICAS ===")
    print("1. NOT")
    print("2. AND")
    print("3. OR")
    print("4. XOR")
    print("5. MUX (Multiplexor)")
    print("6. DMUX (Demultiplexor)")
    print("7. NOT16")
    print("8. AND16")
    print("9. OR16")
    print("10. MUX16")
    print("11. OR8WAY")
    print("12. MUX4Way16")
    print("13. MUX8Way16")
    print("14. DMUX4Way")
    print("15. DMUX8Way")
    print("0. Salir")


def ejecutar_opcion(opcion):
    if opcion == "1":
        a = int(input("Ingrese el valor de A (0 o 1): "))
        not_chip(a)
    elif opcion == "2":
        a = int(input("Ingrese A (0 o 1): "))
        b = int(input("Ingrese B (0 o 1): "))
        and_chip(a, b)
    elif opcion == "3":
        a = int(input("Ingrese A (0 o 1): "))
        b = int(input("Ingrese B (0 o 1): "))
        or_chip(a, b)
    elif opcion == "4":
        a = int(input("Ingrese A (0 o 1): "))
        b = int(input("Ingrese B (0 o 1): "))
        xor_chip(a, b)
    elif opcion == "5":
        a = int(input("Ingrese A (0 o 1): "))
        b = int(input("Ingrese B (0 o 1): "))
        sel = int(input("Ingrese selector (0 o 1): "))
        mux_chip(a, b, sel)
    elif opcion == "6":
        a = int(input("Ingrese A (0 o 1): "))
        sel = int(input("Ingrese selector (0 o 1): "))
        dmux_chip(a, sel)
    elif opcion == "7":
        not16_chip()
    elif opcion == "8":
        and16_chip()
    elif opcion == "9":
        or16_chip()
    elif opcion == "10":
        mux16_chip()
    elif opcion == "11":
        or8way()
    elif opcion == "12":
        mux4way16()
    elif opcion == "13":
        mux8way16()
    elif opcion == "14":
        dmux4way()
    elif opcion == "15":
        dmux8way()
    elif opcion == "0":
        print("Saliendo del programa...")
        return False
    else:
        print(" Opción no válida, intenta de nuevo.")
    
    return True


# 🔹 **Ejecución del Menú**
while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if not ejecutar_opcion(opcion):
        break















# 🔹 **Ejecución de pruebas**
print("\n=== PRUEBAS ===")
not_chip()
and_chip()
or_chip()
xor_chip()
mux_chip()
dmux_chip()
not16_chip()
and16_chip()
or16_chip()
mux16_chip()
or8way()
mux4way16()
mux8way16()
dmux4way()
dmux8way()