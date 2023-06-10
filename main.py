#Импорт
from flask import Flask, render_template, request
from info import subject, password, sender
from email.mime.text import MIMEText
import smtplib
import ssl


app = Flask(__name__)

def result_calculate(size, lights, device):
    #Переменные для энергозатратности приборов
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5   
    return size * home_coef + lights * light_coef + device * devices_coef 

#Первая страница
@app.route('/')
def index():
    return render_template('index.html')
#Вторая страница
@app.route('/<size>')
def lights(size):
    return render_template(
                            'lights.html', 
                            size=size
                           )

#Третья страница
@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
                            'electronics.html',                           
                            size = size, 
                            lights = lights                           
                           )

#Расчет
@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html', 
                            result=result_calculate(int(size),
                                                    int(lights), 
                                                    int(device)
                                                    )
                        )
#Форма
@app.route('/form')
def form():
    return render_template('form.html')

# отправка сообщения на почту
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

#Результаты формы
@app.route('/submit', methods=['POST'])
def submit_form():
    global email
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    # запись в txt файл
    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write('Ваше имя: ' + name + '\n' + 'Ваша электронная почта: ' + email + '\n' + 'Ваш адрес: ' + address + '\n' + 'Ваша дата: ' + date)
    # функция отправки сообщения на почту
    send_email(f'''
        Ваше имя: {name}
        Ваша электронная почта: {email}
        Ваш адрес: {address}
        Ваша дата: {date}
    ''')
    # здесь вы можете сохранить данные или отправить их по электронной почте
    return render_template('form_result.html', 
                           #Помести переменные
                           name=name,
                           email=email,
                           address=address,
                           date=date
                           )
    

app.run(debug=True)
