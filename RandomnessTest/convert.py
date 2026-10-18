with open("my_random_bits_4.txt") as f:
    bits = "".join(line.strip() for line in f if line.strip())

# Convert to bytes
byte_array = int(bits, 2).to_bytes((len(bits) + 7)//8, byteorder="big")

with open("my_random_bit_4.bin", "wb") as f:
    f.write(byte_array)
