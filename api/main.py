# -*- coding: utf-8 -*-
"""
api.ipynb
"""

#pip install flask-restx

from flask import Flask, jsonify
from sqlalchemy import create_engine
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields

user = "root"
passw = "123456"
host = "34.175.38.220"
database = "main"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'The famous REST API with FLASK!',
    description = """
        This RESTS API is an API to built with FLASK
        and FLASK-RESTX libraries
        """,
    contact = "gustavom@faculty.ie.edu",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

customer = Namespace('customer',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customer)

@customer.route("/customers")
class get_all_users(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customer
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customer.route("/customers/<string:id>")
@customer.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customer
            WHERE customer_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

article = Namespace('article',
    description = 'All operations related to articles',
    path='/api/v1')
api.add_namespace(article)

@article.route("/articles")
class get_all_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM article
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@article.route("/articles/<string:id>")
@article.doc(params = {'id': 'The ID of the user'})
class select_article(Resource):

    @api.response(404, "ARTICLE not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM article
            WHERE article_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

transaction = Namespace('transaction',
    description = 'All operations related to transactions',
    path='/api/v1')
api.add_namespace(transaction)

@transaction.route("/transactions")
class get_all_transactions(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transaction
            LIMIT 1000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True)