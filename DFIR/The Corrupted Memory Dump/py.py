import os
import numpy as np

FLAG = "MED{m3m0ry_15_4_5c13n7ific_4r7f4c7}"  
FAKE_FLAGS = [
    "MED{f4k3_fl4g_1}",
    "MED{f4k3_fl4g_2}",
    "MED{f4k3_fl4g_3}"
]
DUMP_SIZE = 2 * 1024 * 1024

# 1. Create a fake memory dump with random data
dump = np.random.bytes(DUMP_SIZE)

# 2. Insert fake ELF header (to mislead)
elf_header = (
    b"\x7fELF\x02\x01\x01" + b"\x00" * 9 + 
    b"\x02\x00" + b"\x3e\x00" + b"\x01\x00\x00\x00"
)
dump = elf_header + dump[len(elf_header):]

xor_key_fake = 0x55
for fake_flag in FAKE_FLAGS:
    fake_offset = np.random.randint(0x20000, DUMP_SIZE - len(fake_flag))
    encrypted_fake_flag = bytes([ord(c) ^ xor_key_fake for c in fake_flag])
    dump = dump[:fake_offset] + encrypted_fake_flag + dump[fake_offset + len(encrypted_fake_flag):]

heap_start = 0x10000
xor_key_real = 0xAA
encrypted_flag = bytes([ord(c) ^ xor_key_real for c in FLAG])
dump = dump[:heap_start] + encrypted_flag + dump[heap_start + len(encrypted_flag):]

# 5. Save as "corrupted_dump.bin"
with open("corrupted_dump.bin", "wb") as f:
    f.write(dump)

print("[+] Generated 'corrupted_dump.bin'")
print(f"[+] Real flag hidden at offset 0x{heap_start:04x} (XOR key: 0x{xor_key_real:02x})")
print(f"[+] Fake flags XOR-encoded with key 0x{xor_key_fake:02x}")