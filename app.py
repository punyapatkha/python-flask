import os
from flask import Flask
from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import json


app = Flask(__name__)

json_key = os.environ.get('sakey', None)
service_account_info = json.loads(json_key)
# service_account_info = a
# build credentials with the service account dict
creds = firebase_admin.credentials.Certificate(service_account_info)
# initialize firebase admin
firebase_app = firebase_admin.initialize_app(creds)
db = firestore.client()


@app.route('/')
def hello():
    return 'Hello World!'

# test get environment var
@app.route('/2')
def hello2():
    is_prod = os.environ.get('testkey', None)
    return 'Hello World!'+str(is_prod)+'_end'

# test firestore app 
@app.route('/3')
def hello3():
    doc_ref = db.collection(u'users').document(str(datetime.datetime.now()))
    doc_ref.set({
#         u'first': u'puyo',
#         u'last': u'Pablo4',
        u'born': 123
    })
    return 'upload done!'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        doc_ref = db.collection(u'webhookpost').document(str(datetime.datetime.now()))
        doc_ref.set(request.json)
        print("Data received from Webhook is: ", request.json)
        return "Webhook received!"
    
@app.route('/webhook2', methods=['GET'])
def webhook2():
    if request.method == 'GET':
        doc_ref = db.collection(u'webhookget').document(str(datetime.datetime.now()))
        doc_ref.set({
        u'born': 123
    })
        print("Data received from Webhook is: ")
        return "Webhook received!"
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    
    




