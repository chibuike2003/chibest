Thanks for downloading this template!

Template Name: iPortfolio
Template URL: https://bootstrapmade.com/iportfolio-bootstrap-portfolio-websites-template/
Author: BootstrapMade.com
License: https://bootstrapmade.com/license/


import os
import logging
import pymysql
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email

# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jhhhiyhihgiuffuufuufuf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chibesttech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize database and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)
