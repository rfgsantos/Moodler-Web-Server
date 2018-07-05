import sys
sys.path.append("../utils")
sys.path.append("../dao")
from flask import Flask, jsonify, request
from recomendation_dao import RecomendationDao
database_connector = DatabaseConnector()
recomendationdao = RecomendationDao(database_connector)

@app.route('/recomendation', methods=['GET'])
def get_all_recomendation():
    return jsonify(recomendationdao.get_all_recomendation())

@app.route('/recomendation/<int:id>', methods=['GET'])
def get_recomendation_by_id(id):
    return jsonify(recomendationdao.get_recomendation_by_id(id))

@app.route('/recomendation/insert', methods=['GET'])
def insert_recomendation():
    return jsonify(recomendationdao.insert_recomendation(request.json))

@app.route('/recomendation/delete/<int:id>', methods=['GET'])
def delete_recomendation(id):
    return jsonify(recomendationdao.delete_recomendation(id))