from flask import Blueprint, current_app, request
from model import HELP, DBSession
from user.model import User
import json

help = Blueprint('help', __name__, template_folder='')

@help.route('/help/detail/<id>', methods=['GET'])
def detail(id):
	try:
		print id
	except Exception, e:
		current_app.logger.error(e)
		
	return 'success'

@help.route('/help/publish/<ukey>', methods=['POST'])
def publish(ukey):
	try:
		type = request.form['type']
		title = request.form['title']
		description = request.form['description']
		offer = request.form['offer']
		session = DBSession()
		user = session.query(User).filter(User.user_key==ukey).one()
		new_help = HELP(type=type, title=title, description=description, offer=offer, uid=user.uid)
		session.add(new_help)
		session.commit()
		session.close()
		return 'success'
	except Exception, e:
		current_app.logger.error(e)
		return 'error'

@help.route('/help/history/<ukey>')
def history(ukey):
	try:
		db_session = DBSession()
		user = db_session.query(User).filter(User.user_key==ukey).one()
		list = db_session.query(HELP).filter(HELP.uid==user.uid).all()
		final = []
		for one in list:
			final.append({'id':one.id, 'title':one.title})
		return json.dumps(final)
	except Exception, e:
		current_app.logger.error(e)
		return 'error'
