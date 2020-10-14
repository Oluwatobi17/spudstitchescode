pip install requests


import requests

def index(request):
	headers = {'app_id': 'adsfaeq898433e', 'app_key': settings.PAYSTACK_API}
	url = 'https://facebook.com/getjson/'
	response = requests.get(url, headers=headers)

	data = {
		'title': 'Hello',
		'amount': 494.43
	}
	responseP = requests.post(url, headers=headers, data=data)
	result = response.json()


	#####

	status = response.status_code