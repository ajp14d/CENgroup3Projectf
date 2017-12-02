#database for users

import shelve
import re
import requests

num = 1

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
			#data = {user : [{'name' : name, 'password' : password}]}
			agendaList = []
			data[user] = {'name' : name, 'password' : password, 'agenda' : agendaList}
	except KeyError:
		return "KeyError"

	data.close()


def usrAgenda(user, eventName, eventType, compName, attire, additional):
	try:
		#open the database
		data = shelve.open('acct.db', writeback = True)
		#set the list to the user's existing list if it exists
		agendaList = data[user]['agenda']
		global num

		#store the agenda information in a dict
		agenda = {'id' : num,
				  'eventName' : eventName,
			  	  'eventType' : eventType,
			  	  'compName' : compName,
			      'attire' : attire,
			  	  'additional' : additional}

		print agenda
		#append to the agenada list
		agendaList.append(agenda)
		#update it in the database
		data[user]['agenda'] = agendaList
		num = num + 1

		print num
		data.close()
		print "successful"
		return "Created successfully"
	except:
		print "failure"
		return "Failed to create"

def getAgenda(user):
	data = shelve.open('acct.db', writeback = True)
	agendaList = data[user]['agenda']
	print agendaList

	data.close()
	return agendaList
