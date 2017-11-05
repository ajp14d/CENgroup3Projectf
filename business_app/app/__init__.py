from flask import Flask

#Create a Flask application
b_app = Flask(__name__)

#Get view for the website
from app import views
