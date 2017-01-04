from flask import Flask, request
from help.help import help
from user.user import user

app = Flask(__name__)
app.register_blueprint(help)
app.register_blueprint(user)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run('127.0.0.1', '9000')
