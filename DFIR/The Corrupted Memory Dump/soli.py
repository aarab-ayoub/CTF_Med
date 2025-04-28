# Save this as xor_brute.py and run: python3 xor_brute.py
with open("corrupted_dump.bin", "rb") as f:
    data = f.read()

for key in range(256):
    decoded = bytes([b ^ key for b in data])
    if b"MED{" in decoded:
        print(f"Found potential flag with key {key}:")
        print(decoded.decode(errors="ignore").split("MED{")[1].split("}")[0])
        break

