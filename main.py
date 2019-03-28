from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/')
def home():
    return '<h1>Hello world!</h1>'


if __name__ == '__main__':
    app.run()


#TODO: Add session teardown and rehook into db.py so session is controlled by SQLAlchemy not flask