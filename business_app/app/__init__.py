from flask import Flask

#implementation of the Flask library to house our database

#Create a Flask application
b_app = Flask(__name__)

#Get view for the website
from app import views
