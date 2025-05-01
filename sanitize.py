#!/usr/bin/env python3
import re
import os

# Create necessary directories and files for the challenge
def setup_challenge():
    # Create a secret directory
    os.makedirs("secret_files", exist_ok=True)
    
    # Create a flag file
    with open("secret_files/flag.txt", "w") as f:
        f.write("flag{p4th_s4n1t1z4t10n_byp4ss3d}")
    
    # Create some decoy files
    with open("public_files.txt", "w") as f:
        f.write("Nothing interesting here, keep looking!")

# Function to sanitize the file path
def sanitize_path(user_input):
    # Sanitize: Remove any instance of "../", "~", "/" at beginning, and "//"
    sanitized = re.sub(r'\.\.\/', '', user_input)  # Remove ../
    sanitized = re.sub(r'~', '', sanitized)        # Remove ~
    sanitized = re.sub(r'^/', '', sanitized)       # Remove leading /
    sanitized = re.sub(r'\/\/', '/', sanitized)    # Replace // with /
    
    return sanitized

# Main function to run the challenge
def run_challenge():
    print("=== File Reader Service ===")
    print("I'll read any file you request, but I'm careful about security!")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("Enter file path to read: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Sanitize the user input
        sanitized_path = sanitize_path(user_input)
        print(f"[DEBUG] Sanitized path: {sanitized_path}")
        
        try:
            # Try to open and read the file
            with open(sanitized_path, 'r') as file:
                content = file.read()
                print("\n=== File Content ===")
                print(content)
                print("====================\n")
        except FileNotFoundError:
            print(f"Error: File '{sanitized_path}' not found!")
        except IsADirectoryError:
            print(f"Error: '{sanitized_path}' is a directory, not a file!")
        except PermissionError:
            print(f"Error: Permission denied to read '{sanitized_path}'!")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    setup_challenge()
    run_challenge()