import sys
sys.path.append("../utils")
sys.path.append("../dao")
from flask import Flask, jsonify, request
from reaction_dao import ReactionDao
database_connector = DatabaseConnector()
reactiondao = ReactionDao(database_connector)

@app.route('/reaction', methods=['GET'])
def get_all_reaction():
    return jsonify(reactiondao.get_all_reaction())

@app.route('/reaction/<int:id>', methods=['GET'])
def get_reaction_by_id(id):
    return jsonify(reactiondao.get_reaction_by_id(id))

@app.route('/reaction/insert', methods=['GET'])
def insert_reaction():
    return jsonify(reactiondao.insert_reaction(request.json))

@app.route('/reaction/delete/<int:id>', methods=['GET'])
def delete_reaction(id):
    return jsonify(reactiondao.delete_reaction(id))