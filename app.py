import json
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class JsonFavorite:
    def __init__(self, filename=None, userId=None, readJsonFile=True) -> None:
        filename = 'favorites.json' if filename == None else filename
        self.userId = userId
        self.filename = "./data/{}".format(
            filename) if userId == None else "../data/{}/{}".format(userId, filename)
        self.data = self.readJson() if readJsonFile else {}

    @property
    def GetJson(self):
        return self.data

    def readJson(self):
        with open(self.filename, "r") as openfile:
            data = json.load(openfile)
        return data

    def WriteJson(self, data=None):
        self.data = data if data != None else self.data
        with open(self.filename, "w") as outfile:
            json.dump(self.data, outfile)

    def EmptyJson(self):
        self.data = {}
        self.WriteJson()


@app.route('/favorites')
@cross_origin()
def get_favorites():
    jsonfile = JsonFavorite()
    return jsonfile.GetJson


@app.route('/favorites', methods=['POST'])
@cross_origin()
def post_favorites():
    jsonfile = JsonFavorite()
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        jsonfile.WriteJson(json)
        return {'status': 'success'}
    else:
        return {'status': 'Content-Type not supported!'}


@app.route('/symbols')
@cross_origin()
def symbols():
    filename = "./data/symbols.json"
    with open(filename, 'r') as openfile:
        data = json.load(openfile)
    return data


if __name__ == '__main__':
    app.run(debug=True)

