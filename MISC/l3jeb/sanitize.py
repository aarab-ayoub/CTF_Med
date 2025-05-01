#!/usr/bin/env python3
import os
import re
import subprocess

os.chdir("l3jeb")
print("Welcome to Sanitization Maze!")
print("Find all flag parts and combine them to escape.")
print("WARNING: Command sanitization is active!\n")

BANNED_CHARS = ['&', ';', '|', '`', '$', '>', '<', '*', '?', '!']
BANNED_COMMANDS = ['find', 'grep', 'cat', 'more', 'less', 'head', 'tail', 'strings', 'xxd', 'hexdump']

found_parts = []

def sanitize_command(cmd):
    for char in BANNED_CHARS:
        if char in cmd:
            return None, "Sanitization error: Character '{}' is not allowed!".format(char)
    
    cmd_parts = cmd.split()
    if not cmd_parts:
        return None, "Empty command"
    
    main_command = cmd_parts[0]
    if main_command in BANNED_COMMANDS:
        return None, "Sanitization error: Command '{}' is blocked!".format(main_command)
    
    allowed_commands = ['ls', 'cd', 'pwd', 'echo', 'file', 'wc', 'du', 'df']
    if main_command not in allowed_commands:
        return None, "Command not recognized: '{}'".format(main_command)
    
    return cmd, None

def check_for_flag_parts(output):
    flag_pattern = r'CTF\{[a-zA-Z0-9_!]+\}'
    flags = re.findall(flag_pattern, output)
    
    for flag in flags:
        if flag not in found_parts:
            found_parts.append(flag)
            print("\n[!] Flag part found: {}".format(flag))
            print("[!] You've found {}/5 flag parts\n".format(len(found_parts)))

while True:
    try:
        cmd = input("\n> ")
        if cmd.lower() == "exit" or cmd.lower() == "quit":
            print("Giving up so soon? The flag remains unfound...")
            break
            
        if cmd.lower() == "help":
            print("Available commands: ls, cd, pwd, echo, file, wc, du, df")
            print("Find all flag parts and combine them to escape!")
            continue
            
        if cmd.lower() == "combine":
            if len(found_parts) < 5:
                print("You've only found {}/5 flag parts! Keep searching!".format(len(found_parts)))
            else:
                print("Congratulations! You've combined all flag parts!")
            continue
            
        sanitized_cmd, error = sanitize_command(cmd)
        if error:
            print(error)
            continue
            
        try:
            output = subprocess.check_output(sanitized_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            print(output.strip())
            check_for_flag_parts(output)
        except subprocess.CalledProcessError as e:
            print("Command failed: {}".format(e.output.strip()))
            
    except KeyboardInterrupt:
        print("\nExiting Sanitization Maze. Better luck next time!")
        break
    except Exception as e:
        print("Error: {}".format(str(e)))