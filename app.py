from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'


class MessageForm(FlaskForm):
    mode = RadioField('Режим', choices=[('encode', 'Зашифровать'), ('decode', 'Расшифровать')],
                      default='encode')
    message = StringField('Сообщение', validators=[DataRequired()])
    key = StringField('Ключ')
    submit = SubmitField('Отправить')


def caesar_cipher(text, shift, encode=True):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    if encode:
        table = str.maketrans(alphabet, shifted_alphabet)
    else:
        table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        mode = form.mode.data
        message = form.message.data
        key = form.key.data

        try:
            shift = int(key) if mode == 'decode' else 3
            result = caesar_cipher(message.lower(), shift, encode=(mode == 'encode'))
            if mode == 'encode':
                flash(f'Encoded message: {result}, Key: {shift}', 'success')
            else:
                flash(f'Decoded message: {result}', 'success')
        except ValueError:
            flash('Неверный ключ', 'error')

        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
