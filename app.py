import secrets
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

class MessageForm(FlaskForm):
    mode = RadioField('Mode', choices=[('encode', 'Encode'), ('decode', 'Decode')], default='encode')
    message = StringField('Message', validators=[DataRequired()])
    key = StringField('Key (for decoding only)', validators=[])
    submit = SubmitField('Submit')


def generate_key(length=16):
    return ''.join(secrets.choice(string.ascii_uppercase) for _ in range(length))


def symbol_shift(symbol, key_symbol, encrypt=True):
    n = 26 if ('a' <= symbol <= 'z' or 'A' <= symbol <= 'Z') else 32

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

    new_symbol = chr((ord(symbol) - base + key_offset) % n + base)
    return new_symbol


def vigenere_cipher(text, key, encrypt=True):
    result = []
    key_index = 0

    for symbol in text:
        if symbol.isalpha():
            key_symbol = key[key_index % len(key)]
            if symbol.isalpha() and key_symbol.isalpha():
                result_symbol = symbol_shift(symbol, key_symbol, encrypt)
                result.append(result_symbol)
                key_index += 1
            else:
                result.append(symbol)
        else:
            result.append(symbol)

    return ''.join(result)


def encrypt(message, key):
    return vigenere_cipher(message, key, encrypt=True)


def decrypt(ciphertext, key):
    return vigenere_cipher(ciphertext, key, encrypt=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        mode = form.mode.data
        message = form.message.data
        key = form.key.data if form.key.data else generate_key()

        if mode == 'encode':
            encrypted_vigenere = encrypt(message, key)
            flash(f'Encoded message: {encrypted_vigenere}, Key: {key}', 'success')
        else:
            final_decrypted = decrypt(message, key)
            flash(f'Decoded message: {final_decrypted}', 'success')

        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
