from flask import Blueprint
from model import HELP, DBSession

help = Blueprint('help', __name__, template_folder='')

@help.route('/help/detail/<id>', methods=['GET'])
def detail(id):
	try:
		print id
	except Exception, e:
		app.logger.error(e)
		
	return 'success'

@help.route('/help/publish', methods=['POST'])
def publish():
	try:
		print request.form
		type = request.form['type']
		title = request.form['title']
		description = request.form['description']
		offer = request.form['offer']
		session = DBSession()
		new_help = HELP(type=type, title=title, description=description, offer=offer)
		session.add(new_help)
		session.commit()
		session.close()
		return 'success'
	except Exception, e:
		app.logger.error(e)
		return 'error'
