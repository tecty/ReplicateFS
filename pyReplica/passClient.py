#!/usr/bin/env python

from journal import Journal, JournalController

jc = JournalController()


if __name__ == "__main__":
    
    from flask import Flask,jsonify
    app = Flask(__name__)

    @app.route("/")
    def list():
        return jsonify(jc.getAllJournal())

    @app.route('/', methods = ['POST'])
    def create():
        journal = request.get_json()
        return jsonify(jc.createJournal(journal.ops, journal))


    app.run(
        host = '0.0.0.0',
        port= '8080',
    )