#!/usr/bin/env python3

from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_github import GitHub

app = Flask(__name__)

app.config.from_pyfile('settings.cfg', silent=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
github = GitHub(app)

from heyvector.auth_module import routes
