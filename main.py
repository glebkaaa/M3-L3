import ssl
import smtplib
import requests
from flask import Flask, render_template, request
from info import password, sender
from bs4 import BeautifulSoup


app = Flask(__name__)


def result_calculate(size, lights, device):
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5
    return size * home_coef + lights * light_coef + device * devices_coef


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<size>')
def lights(size):
    return render_template(
        'lights.html',
        size=size
    )


@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
        'electronics.html',
        size=size,
        lights=lights
    )


@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    global url
    url = f'http://127.0.0.1:5000/{size}/{lights}/{device}'
    return render_template('end.html',
                           result=result_calculate(int(size),
                                                   int(lights),
                                                   int(device)
                                                   )
                           )


@app.route('/form')
def form():
    return render_template('form.html')


def send_email(message):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login(sender, password)
        server.sendmail(sender, email, message.encode('utf-8'))
        server.quit()
        return 'The message was sent successfully'
    except Exception as e:
        return f'An error occurred! The error is "{e}"'


@app.route('/submit', methods=['POST'])
def submit_form():
    global email
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find('span', class_='result_energy').text
    count = soup.find('span', class_='count_energy').text

    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write(
            f'Ваше имя: {name} \nВаша электронная почта: {email} \nВаш адрес: {address} \nВаша дата: {date} \nВаш результат: {result} \nКоличество кВт⋅ч: {count}')

    send_email(f'''
        Ваше имя: {name}
        Ваша электронная почта: {email}
        Ваш адрес: {address}
        Ваша дата: {date}
        Ваш результат: {result}
        Количество кВт⋅ч: {count}
    ''')
    return render_template('form_result.html',
                           name=name,
                           email=email,
                           address=address,
                           date=date
                           )


app.run(debug=True)
