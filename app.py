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

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jhhhiyhihgiuffuufuufuf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chibesttech'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['UPLOAD_FOLDER'] = 'uploads'

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Define the Testimonial model
    class Testimonial(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), nullable=False)
        profile_picture = db.Column(db.String(150), nullable=False)
        message = db.Column(db.Text, nullable=False)

    # Define the Contact model
    class Contact(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        subject = db.Column(db.String(100), nullable=False)
        message = db.Column(db.Text, nullable=False)

    # Define the TestimonialForm form
    class TestimonialForm(FlaskForm):
        name = StringField('Your Name', validators=[DataRequired()])
        email = EmailField('Your Email', validators=[DataRequired(), Email()])
        profile_picture = FileField('Profile Picture', validators=[DataRequired()])
        message = TextAreaField('Remarks', validators=[DataRequired()])

    # Define the ContactForm form
    class ContactForm(FlaskForm):
        name = StringField('Your Name', validators=[DataRequired()])
        email = EmailField('Your Email', validators=[DataRequired(), Email()])
        subject = StringField('Subject', validators=[DataRequired()])
        message = TextAreaField('Message', validators=[DataRequired()])

    # Define the home route
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        form = TestimonialForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

            # Handle file upload
            filename = ''
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        file.save(file_path)
                    except Exception as e:
                        flash(f'Error saving file: {e}', 'error')
                        return render_template('index.html', form=form)

            # Insert into database
            try:
                new_testimonial = Testimonial(
                    name=name,
                    email=email,
                    profile_picture=filename,
                    message=message
                )
                db.session.add(new_testimonial)
                db.session.commit()
                flash('Thank you for your feedback!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving testimonial: {e}', 'error')

            return render_template('index.html', form=form)  # Stay on the same page with success message

        # Handle validation errors
        if form.errors:
            flash('Please complete all required fields.', 'error')

        return render_template('index.html', form=form)

    # Define the contact route
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            message = form.message.data

            # Create a new contact entry
            try:
                new_contact = Contact(name=name, email=email, subject=subject, message=message)
                db.session.add(new_contact)
                db.session.commit()
                flash('Message sent successfully! , we will get back to you as soon as possible', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving contact: {e}', 'error')

            return redirect(url_for('contact'))

        # Handle validation errors
        if form.errors:
            flash('Please complete all required fields.', 'error')

        return render_template('contact.html', form=form)

    # Enable SQLAlchemy logging for debugging
    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)

    return app

# Run the Flask application
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
