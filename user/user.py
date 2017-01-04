from flask import Blueprint, current_app, request, session
import urllib2, urllib, redis, string
from model import USER, DBSession
from random import choice

user = Blueprint('user', __name__, template_folder='')
appid = 'wxdcc618aa716157a0'
secret = '629804200c162c9661454000caf987da'
url = 'https://api.weixin.qq.com/sns/jscode2session?'
session_timeout = 43200 

@user.route('/user/onLogin')
def onLogin():
	try:
		code = request.args.get('code', '')
		if code:
			values = {'appid':appid, 'secret':secret, 'js_code':code, 'grant_type':'authorization_code'}	
			url2 = url + urllib.urlencode(values)
			response = urllib2.urlopen(url2)
			resp = response.read()
			redis_client = redis.Redis(host='172.17.0.53',port=6379)
			user_session = make_session()
			redis_client.setex(user_session, resp, session_timeout)
			session['user_key'] = user_session
		return user_session 
	except Exception, e:
		current_app.logger.error(e)
		return 'error'


def make_session():
	user_key = ''.join([choice(string.ascii_letters+string.digits) for i in range(36)])
	return user_key

def get_user_info():
	return userinfo
