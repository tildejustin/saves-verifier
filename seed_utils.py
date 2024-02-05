from fixedint import Int64, Int32


def to_bin(x, bits: int) -> str:
    x = bin(x)[2:]
    if x[0] == "b":
        return twos_complement(x[1:], bits)
    else:
        return x


def twos_complement(x: str, bits: int) -> str:
    for i in range(bits - len(x)):
        x = "0" + x
    x_list = list(x)
    for i in range(bits):
        if x_list[bits - i - 1] == "1":
            x_list[bits - i - 1] = "0"
        else:
            x_list[bits - i - 1] = "1"
    return "".join(x_list)


def unsigned_right_shift_32(x: int) -> int:
    if x >= 0:
        return x >> 32
    else:
        e = to_bin(x, 64)
        if len(e) > 32:
            return int(e[:32], 2)
        else:
            return x


def is_random(seed) -> bool:
    a = Int64(seed)
    b = Int64(18218081)
    c = Int64(1) << 48
    d = Int64(7847617)
    e = ((d * ((unsigned_right_shift_32(a) * 24667315 + b * Int32(a) + 67552711) >> 32) - b *
          ((-4824621 * unsigned_right_shift_32(a) + d * Int32(a) + d) >> 32)) - 11) * Int64(0xdfe05bcb1365) % c
    return ((((Int64(0x5deece66d) * e + 11) % c) >> 16) << 32) + Int32(((Int64(0xbb20b4600a69) * e + Int64(0x40942de6ba)) % c) >> 16) == a
