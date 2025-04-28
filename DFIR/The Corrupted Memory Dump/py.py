import os
import numpy as np

FLAG = "MED{m3m0ry_forens1cs_1s_fun}"  
DUMP_SIZE = 2 * 1024 * 1024  # 2MB "memory dump"

# 1. Create a fake memory dump with random data
dump = np.random.bytes(DUMP_SIZE)

# 2. Insert fake ELF header (to mislead)
elf_header = (
    b"\x7fELF\x02\x01\x01" + b"\x00" * 9 + 
    b"\x02\x00" + b"\x3e\x00" + b"\x01\x00\x00\x00"
)
dump = elf_header + dump[len(elf_header):]

# 3. Hide flag in XOR-encrypted heap section
heap_start = 0x10000
xor_key = 0xAA
encrypted_flag = bytes([ord(c) ^ xor_key for c in FLAG])
dump = dump[:heap_start] + encrypted_flag + dump[heap_start + len(encrypted_flag):]

# 4. Save as "corrupted_dump.bin"
with open("corrupted_dump.bin", "wb") as f:
    f.write(dump)

print("[+] Generated 'corrupted_dump.bin'")
print(f"[+] Flag hidden at offset 0x{heap_start:04x} (XOR key: 0x{xor_key:02x})")