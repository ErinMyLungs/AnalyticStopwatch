from flask import Flask, render_template
from src.config import DevConfig

app = Flask(__name__, template_folder='templates')
app.config.from_object(DevConfig)


@app.route('/')
def stopwatch():
    return render_template('stopwatch.html')


if __name__ == '__main__':
    app.run()


#TODO: Add session teardown and rehook into db.py so session is controlled by SQLAlchemy not flask
