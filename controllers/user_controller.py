import sys
from flask import jsonify, request
from dao.user_dao import UserDao
from main_app import app

userdao = UserDao()

@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(userdao.get_all_users())

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return jsonify(userdao.get_user_by_id(id))

@app.route('/users/insert', methods=['GET'])
def insert_user():
    return jsonify(userdao.insert_user(request.json))

@app.route('/users/delete/<int:id>', methods=['GET'])
def delete_user(id):
    return jsonify(userdao.delete_user(id))

