from flask import Flask
from flask import render_template
from lib.contract import *

import time

app = Flask(__name__)

# routers
@app.route('/<name>')
def hello_world(name=None):
	return render_template('hello.html',name=name)


# routers
@app.route('/accounts')
def accounts(name=None):
	return render_template('accounts.html',accounts=[{'address':'0xca35b7d915458ef540ade6068dfe2f44e8fa733c','count':1},{'address':'0xf6e9e5a47cea2ec4ef1e2eb8307e783f1394817b','count':1}])


# routers
@app.route('/evidence')
def evidence(name=None):
	return render_template('evidence.html',accounts=[{'address':'0xca35b7d915458ef540ade6068dfe2f44e8fa733c','count':1},{'address':'0xf6e9e5a47cea2ec4ef1e2eb8307e783f1394817b','count':1}])


if __name__ == "__main__":
	get_token()
	save_evidence('an_evidence_hash')
	get_evidence('an_evidence_hash')
	get_users()
	app.run(debug=True)
