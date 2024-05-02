import secrets
from flask import Flask, request, jsonify
import string

app = Flask(__name__)


def generate_key(length=16):
    return ''.join(secrets.choice(string.ascii_uppercase) for _ in range(length))


def symbol_shift(symbol, key_symbol, encrypt=True):
    num_letters = 26 if ('a' <= symbol <= 'z' or 'A' <= symbol <= 'Z') else 32

    if symbol.islower():
        base = ord('a') if 'a' <= symbol <= 'z' else ord('а')
    elif symbol.isupper():
        base = ord('A') if 'A' <= symbol <= 'Z' else ord('А')
    else:
        return symbol

    if key_symbol.islower():
        key_base = ord('a') if 'a' <= key_symbol <= 'z' else ord('а')
    elif key_symbol.isupper():
        key_base = ord('A') if 'A' <= key_symbol <= 'Z' else ord('А')

    key_offset = ord(key_symbol) - key_base
    if not encrypt:
        key_offset = -key_offset

    new_symbol = chr((ord(symbol) - base + key_offset) % num_letters + base)
    return new_symbol


def vigenere_cipher(text, key, encrypt=True):
    result = []
    key_index = 0

    for symbol in text:
        if symbol.isalpha():
            key_symbol = key[key_index % len(key)]
            if symbol.isalpha() and key_symbol.isalpha():
                result_char = symbol_shift(symbol, key_symbol, encrypt)
                result.append(result_char)
                key_index += 1
            else:
                result.append(symbol)
        else:
            result.append(symbol)

    return ''.join(result)


def encrypt(message, key):
    return vigenere_cipher(message, key, encrypt=True)


def decrypt(message, key):
    return vigenere_cipher(message, key, encrypt=False)


@app.route('/encode', methods=['POST'])
def encode():
    data = request.json
    message = data['message']
    key = generate_key()
    encoded_message = encrypt(message, key)
    return jsonify({'encoded_message': encoded_message, 'key': key})


@app.route('/decode', methods=['POST'])
def decode():
    data = request.json
    message = data['message']
    key = data['key']
    decoded_message = decrypt(message, key)
    return jsonify({'decoded_message': decoded_message})


if __name__ == '__main__':
    app.run(debug=True)
