#coding:utf-8
from flask import Blueprint, current_app, request
import urllib2, urllib, redis, string, json
from model import User, UserSession, DBSession
from random import choice

user = Blueprint('user', __name__, template_folder='')
appid = 'wxdcc618aa716157a0'
secret = '629804200c162c9661454000caf987da'
url = 'https://api.weixin.qq.com/sns/jscode2session?'
session_timeout = 2592000

@user.route('/user/onLogin', methods=['GET', 'POST'])
def onLogin():
	try:
		db_session = DBSession()
		if request.method == 'POST':
				data = json.loads(request.data)
				userinfo = data['userInfo']
				if data['code']:
					values = {'appid':appid, 'secret':secret, 'js_code':data['code'], 'grant_type':'authorization_code'}	
					url2 = url + urllib.urlencode(values)
					response = urllib2.urlopen(url2)
					resp = response.read()
					resp_json = json.loads(resp)
					openid = resp_json['openid']
					user_key = make_session()
					##获取openid & session_key

					user = db_session.query(User).filter(User.uid==openid).count()
					if not user:
						new_user = User(uid=openid, nick_name=userinfo['nickName'], avatar_url=userinfo['avatarUrl'], gender=userinfo['gender'], provice=userinfo['province'], city=userinfo['city'], country=userinfo['country'], user_key=user_key)
						db_session.add(new_user)
					else:
						db_session.query(User).filter(User.uid==openid).update({User.user_key:user_key})
					db_session.commit()
					##存储用户信息

					redis_client = redis.Redis(host='172.17.0.53',port=6379)
					redis_client.setex(user_key, resp, session_timeout)
					##缓存session

					user_session = UserSession(user_key=user_key, page='page/user/index/index')
					db_session.add(user_session)
					db_session.commit()
					##存储用户session

					return user_key 
				else:
					return 'code empty'
		else:
			user_key = request.args.get('user_key', '')
			user_session = db_session.query(UserSession).filter(UserSession.user_key==user_key).one()
			user = db_session.query(User).filter(User.user_key==user_key).one()
			return (json.dumps({'page':user_session.page, 'userInfo':{'nickName':user.nick_name, 'avatarUrl':user.avatar_url}}),) 
			##返回用户最后页面位置

		db_session.close()
			
			
	except Exception, e:
		current_app.logger.error(e)
		return 'error'


def make_session():
	user_key = ''.join([choice(string.ascii_letters+string.digits) for i in range(36)])
	return user_key

