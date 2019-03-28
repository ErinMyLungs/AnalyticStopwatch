from main import app
from db import Session
from models import User

# TODO: likely to die because db management easier in shell

@app.shell_context_processor
def make_shell_context():
    return dict(app=Session(), db=db, User=User)
