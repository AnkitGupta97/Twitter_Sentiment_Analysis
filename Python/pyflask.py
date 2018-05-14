from flask import Flask
from flask import request

import sentimentAnalysis
app = Flask(__name__)

@app.route('/')
def flask_start():
    return 'Flask Server is running'

@app.route('/startquery', methods=['POST'])
# sentimentAnalysis.startQuery()
def flask_startQuery():
    # return str("server got query for : " + request.form['query'])
    if 'query' in request.get_json():
        query =  request.get_json()['query']
        print("query at flask : " + query)
        return sentimentAnalysis.startQuery(query)    
    # return "hi there" + str(request.form.get('query'))
    return "error fetching query at flask"
