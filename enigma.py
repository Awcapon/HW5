import sys
import json
import os
ABC = 26

class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map.copy()
        self.reverse_hash_map = {v : k for k, v in self.hash_map.items()}
        self.wheels = wheels.copy()
        self.reflector_map = reflector_map.copy()

    def encrypt(self, message):
        encrypted_message = ""
        count = 0
        for line in message:
            tempwheels = self.wheels.copy()
            for char in line:
                if char.isalpha() and char.islower():
                    count += 1
                    encrypted_char = self.encrypt_one_character(tempwheels, char)
                    encrypted_message += encrypted_char
                else:
                    encrypted_message += char
                tempwheels = shift_wheels(tempwheels, count)

        return encrypted_message

    def encrypt_one_character(self, wheels, c):
        w1, w2, w3 = wheels
        i = self.hash_map[c]
        if (((w1 * 2) - w2 + w3) % ABC == 0):
            i += 1
        else:
            i += ((w1 * 2) - w2 + w3) % ABC
        i = i % ABC

        c1 = self.reverse_hash_map[i]
        c2 = self.reflector_map[c1]

        i = self.hash_map[c2]

        if (((w1 * 2) - w2 + w3) % ABC == 0):
            i -= 1
        else:
            i -= ((w1 * 2) - w2 + w3) % ABC
        i = i % ABC

        c3 = self.reverse_hash_map[i]

        return c3

def shift_wheels(wheels, num_of_encryptions):
    wheels[0] = 1 if wheels[0] + 1 > 8 else wheels[0] + 1
    wheels[1] = wheels[1] * 2 if num_of_encryptions % 2 == 0 else wheels[1] - 1
    if(num_of_encryptions % 10 == 0):
        wheels[2] = 10
    elif(num_of_encryptions % 3 == 0):
        wheels[2] = 5
    else:
        wheels[2] = 0

    return wheels

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)

        if not all(key in data for key in ['hash_map', 'wheels', 'reflector_map']):
            raise ValueError("Missing one or more required keys in the JSON data")

        return Enigma(hash_map=data['hash_map'], wheels=data['wheels'], reflector_map=data['reflector_map'])

    except FileNotFoundError:
        print(f"Error: The file at {path} does not exist.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file at {path} contains invalid JSON.")
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
        exit(1)

    try:
        args = sys.argv[1:]

        config_file = args[args.index('-c') + 1]
        input_file = args[args.index('-i') + 1]
        output_file = args[args.index('-o') + 1] if '-o' in args else None

        enigma = load_enigma_from_path(config_file)

        with open(input_file, 'r') as f:
            input_data = f.readlines()


        Encrypted_msg = enigma.encrypt(input_data)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(Encrypted_msg)
        else:
            print(Encrypted_msg)

    except FileNotFoundError:
        print(f"The file was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"The enigma script has encountered an error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()