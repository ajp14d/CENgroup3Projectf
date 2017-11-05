#database for users

import shelve
import re
import requests

def userAcct(name, user, password):
	print("conncected")
	try:
		print("trying")
		data = shelve.open('acct.db', writeback = True)
		#if this user is not a new user, fail
		if user in data:
			data.close()
			print('failure')
			return "failure"
		#else create the password and user
		else:
			print("IN DB")
			data[user] = {'name' : name, 'password' : password}
	except KeyError:
		return "KeyError"

	data.close()
