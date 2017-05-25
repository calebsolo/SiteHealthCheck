import bottle
import pymongo
from bottle import static_file, route, run, template, error
from bson.code import Code


DATABASE_HOST = 'localhost'
DATABASE_NAME = 'NodeList'
DATABASE_PORT = 27017

connection = pymongo.MongoClient(DATABASE_HOST, DATABASE_PORT)
nodes = connection.NodeList.nodes
logs = connection.NodeList.log

@bottle.route('/')
def index():
	returnhosts = []
	cursor = nodes.find({},{'_id':0})
	for host in cursor:
		returnhosts.append(host['NodeName'])

	return bottle.template('index',{"returnhosts":returnhosts})

@bottle.post('/addhost')
def addhost():
	host = bottle.request.forms.get("host")
	if (host == None or host == ""):
		host = None

	nodes.save({"NodeName":host})
	returnhosts = []
	cursor = nodes.find({},{'_id':0})
	for host in cursor:
		returnhosts.append(host['NodeName'])

	#   for document in cursor:
	#	returnhosts.append(document.NodeName)

	return bottle.template('added',{"returnhosts":returnhosts})

@bottle.route('/logs')
def index():
	returnlogs = []
	cursor = logs.find({},{'_id':0})
	for logentry in cursor:
		strLog = logentry['ErrorTime'] + "," + logentry['NodeName'] + "," + logentry['ResponseCode']
		returnlogs.append(strLog)

	return bottle.template('logs',{"returnlogs":returnlogs})

@bottle.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

@bottle.route('/figures/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/figures/')

@bottle.route('/images/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/images/')
#@get('/<filename:re:.*\.css>')
#def stylesheets(filename):
#    return static_file(filename, root='static/')

@bottle.error(404)
def error404(error):
    return 'Nothing here, sorry'

bottle.run(host='0.0.0.0', port=8000, debug=1);
