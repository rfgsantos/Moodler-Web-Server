from flask import Flask, jsonify, request
from dao.reaction_dao import ReactionDao
from main_app import app

reaction_dao = ReactionDao()

@app.route('/reaction', methods=['GET'])
def get_all_reaction():
    return jsonify(reactiondao.get_all_reaction())

@app.route('/reaction/<int:id>', methods=['GET'])
def get_reaction_by_id(id):
    return jsonify(reactiondao.get_reaction_by_id(id))

@app.route('/reaction/insert', methods=['POST'])
def insert_reaction():
    return jsonify(reactiondao.insert_reaction(request.json))

@app.route('/reaction/delete/<int:id>', methods=['GET'])
def delete_reaction(id):
    return jsonify(reactiondao.delete_reaction(id))