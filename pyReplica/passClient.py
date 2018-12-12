#!/usr/bin/env python

from journal import Journal, JournalController
import logging



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    
    jc = JournalController(args.mount)
    



    from flask import Flask,jsonify
    app = Flask('replicaClient')

    @app.route("/")
    def list():
        return jsonify(jc.getAllJournal())

    @app.route('/', methods = ['POST'])
    def create():
        journal = request.get_json()
        return jsonify(jc.createJournal(journal.ops, journal))

    @app.route('/', methods = ['PUT'])
    def commit():
        j_id = request.get_json()['id']
        journal = jc.getJournal(j_id)
        journal.doCommit()
        return True

    app.run(
        host = '0.0.0.0',
        port= '8080',
    )