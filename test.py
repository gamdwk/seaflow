from flask_mail import Mail, Message
from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
mail = Mail(app)
app.config.from_object(DevelopmentConfig)


@app.route('/')
def index():
    message = Message('Hello',
                      recipients=["728882065@qq.com"])
    mail.send(message)


if __name__ == '__main__':
    app.run()
