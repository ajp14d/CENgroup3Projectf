#run this program if you want to see what is stored in the database

import shelve

db = shelve.open('acct.db')
print("print?")
for user in db:
	print user, db[user]	#prints username and attached information

db.close()
