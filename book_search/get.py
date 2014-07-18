from django.contrib.auth.models import Group, User
from django.utils import simplejson
from django.http import HttpResponse

def get_account(requests):
	u = User.objects.all()
	d= {}
	for num, obj in enumerate(u):
		d.update({num:{'fname':obj.first_name,'lname':obj.last_name,'username':obj.username}})
	data = simplejson.dumps(d)
	return HttpResponse(data, mimetype='application/json')


def set_password(requests):
	pass
	


