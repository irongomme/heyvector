#!/usr/bin/env python3

from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_github import GitHub

app = Flask(__name__)
app.secret_key = b'{^TL:wiE@x#@:A%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['GITHUB_CLIENT_ID'] = 'Iv1.7863ea568881bcfe'
app.config['GITHUB_CLIENT_SECRET'] = 'dc553887e49a6ba4a7c9e21a402d02dbbab2e620'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
github = GitHub(app)

from heyvector.auth_module import routes
