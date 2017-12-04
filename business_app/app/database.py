#database for users

import shelve
import re
import requests

#database that saves the users profile and their agenda 

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


def usrAgenda(user, eventName, eventType, location, date, time, compName, attire, additional):
	try:
		#open the database
		data = shelve.open('acct.db', writeback = True)
		#set the list to the user's existing list if it exists
		agendaList = data[user]['agenda']

		if not agendaList:
			num = 1
		else:
			num = agendaList[-1]['id'] + 1

		print ("NUM: ", num)

		#store the agenda information in a dict
		agenda = {'id' : num,
				  'eventName' : eventName,
			  	  'eventType' : eventType,
				  'location' : location,
				  'date' : date,
				  'time' : time,
			  	  'compName' : compName,
			      'attire' : attire,
			  	  'additional' : additional}

		print agenda
		#append to the agenada list
		agendaList.append(agenda)
		#update it in the database
		data[user]['agenda'] = agendaList

		data.close()
		print "agenda successful"
		return "Created successfully"
	except:
		print "agenda failure"
		return "Failed to create"

def getAgenda(user):
	data = shelve.open('acct.db', writeback = True)
	agendaList = data[user]['agenda']
	print agendaList

	data.close()
	return agendaList
