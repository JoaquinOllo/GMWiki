from flask import Flask
from Server import config
import copy
from flask import request
from Constants import ResponseCodes
from Engine import Main

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app

enviroment = config.config['development']


app = create_app(enviroment)


#https://flask.palletsprojects.com/en/1.1.x/quickstart/
#Instructions to run flask server, on windows cmd
#cd ".\GMWiki\Server"
#set FLASK_APP=mainServer.py
#set FLASK_ENV=development
#python -m flask run

responseDefault = {
    "operationSuccess": ResponseCodes.ERROR,
    "links": [],
    "description": "Operation not executed",
    "requestMetadata": {
        "method": "",
        "params": []
    }
}

@app.route('/links/<field>/<value>', methods=['GET', 'DELETE', 'PATCH'])
def links(field, value):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        #seek many links
        response["operationSuccess"] = ResponseCodes.SUCCESS
        response["requestMetadata"]["method"] = request.method
        response["requestMetadata"]["params"].append ({"value": value})
        response["requestMetadata"]["params"].append ({"field": field})
        app.logger.info(Main.getManyByField)
        for link in Main.getManyByField(value, field):
            response['links'].append(link.toJSON())
        return (response, [("Access-Control-Allow-Origin", "*")])
    elif request.method == "DELETE":
        Main.deleteLinkByField(field, value)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        return response
    elif request.method == "PATCH":
        jsonData = request.get_json()
        Main.editLinkPartially(value, jsonData)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        return response

@app.route('/hello')
def hello():
    return 'Hello, World'