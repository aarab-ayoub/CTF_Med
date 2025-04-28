### **1. DFIR (Digital Forensics & Incident Response)**
**Challenge 1: Corrupted Memory Dump (Hard)**  
- **Description**: Analyze a fake memory dump (`corrupted_dump_v2.bin`) with fragmented flag parts (AES, Base64, Zlib).  
- **Skills**: Memory analysis, encryption, data carving.  
- **Hint**: "The key is in the memory itself. Look for 'AES_FLAG:' and 'B64:' markers."  

**Challenge 2: Disk Detective (Medium)**  
- **Description**: A disk image (`disk.img`) has a deleted file containing the flag.  
- **Skills**: File recovery (`photorec`, `fls`), partition analysis.  
- **Hint**: "Check the lost+found directory."  

**Challenge 3: Wireshark Traffic Analysis (Easy)**  
- **Description**: A PCAP file (`traffic.pcap`) contains an exfiltrated flag via DNS tunneling.  
- **Skills**: Wireshark filters, DNS exfiltration.  
- **Hint**: "Look for unusually long DNS queries."  

**Challenge 4: Ransomware Artifacts (Hard)**  
- **Description**: A ransomware-encrypted file (`secret.docx.enc`) and memory dump. Find the decryption key.  
- **Skills**: Volatility, ransomware analysis.  

---

### **2. MISC (Miscellaneous)**
**Challenge 1: Python Frequency Puzzle (Medium)**  
- **Description**: Extract a flag from a WAV file (`secret.wav`) using FFT in Python.  
- **Skills**: Signal processing, Python scripting.  
- **Hint**: "Each character has its own frequency slot."  

**Challenge 2: Image Bit Manipulation (Easy)**  
- **Description**: A PNG image (`puzzle.png`) hides the flag in LSB (Least Significant Bits).  
- **Skills**: Steganography tools (`stegsolve`, `zsteg`).  
- **Hint**: "Use `zsteg` or Python PIL to check RGB values."  

**Challenge 3: Telegram Bot Flag (Medium)**  
- **Description**: A Telegram bot (`@CTF_FlagBot`) gives the flag if you solve a math puzzle.  
- **Skills**: API interaction, automation.  
- **Hint**: "The bot responds to `/start` and `/solve <answer>`."  

**Challenge 4: Expanding Image (Hard)**  
- **Description**: A seemingly tiny image (`tiny.jpg`) expands to reveal the flag when resized.  
- **Skills**: Hex editing, image forensics.  

---

### **3. OSINT (Open-Source Intelligence)**
**Challenge 1: Blurred Website Screenshot (Medium)**  
- **Description**: A blurred screenshot of a darknet site (Ahmia) hides the URL. Find the original.  
- **Skills**: Reverse image search, darknet navigation.  
- **Hint**: "The site sells 'rare books'."  

**Challenge 2: Real Madrid Riddle (Easy)**  
- **Description**: "What is the name of Real Madrid’s stadium before 2023?" Flag: `MED{<answer>}`.  
- **Skills**: Quick Google search.  

**Challenge 3: Google Map Location (Hard)**  
- **Description**: A photo (`location.jpg`) with geotags removed. Find coordinates using shadows/landmarks.  
- **Skills**: Geolocation, Google Earth.  
- **Hint**: "The building has a red roof."  

**Challenge 4: Twitter Clue (Medium)**  
- **Description**: A deleted tweet from `@CTF_HintMaster` contained the flag. Find it via archive.org.  
- **Skills**: Wayback Machine, tweet archiving.  

---

### **Bonus Challenges (Flexible Categories)**
- **DFIR**: "Log Analysis" (Apache logs with hidden flag).  
- **MISC**: "QR Chain" (Multiple QR codes leading to the flag).  
- **OSINT**: "Email Tracing" (Find the flag in a leaked email dump).  

---
