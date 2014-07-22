import os, functions
from flask import Flask, jsonify, request, render_template
from flask.ext import restful
from sqlalchemy import Table, create_engine, schema, func, desc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, template_folder='../app', static_folder='../app/static')
app.debug = True
api = restful.Api(app)

metadata = schema.MetaData()
engine=create_engine('sqlite:////Users/gmoselle/projects/ascension_kit/players.db', echo=False)
metadata.bind = engine
session = sessionmaker(bind=engine)()
games = Table('games', metadata, autoload=True)

@app.route('/')
def index():
    return "hello, world"
    #return render_template('index.html')
