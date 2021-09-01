import hashlib
import random

#global variable
clientId=[]

#user level variable
orderCount=1

#company level variables
searchParameter=0
buy=0
sell=0
bid={}	
ask={}

class user:
	def __init__(self):
		self.generateID()
	pass


def hid(a):	#funct to produce hash
	key=hashlib.sha256()
	key.update(a.encode('utf8'))
	return(key.hexdigest())

class userClass:
	def __init__(self):
		
		# userId='NA'
		self.generateID()
		self.password='NA'
		self.funds=0.0
		self.orderHistory={
			#FORMAT FOR OREDER HISTORY
			# 000:{'Product':'',
			# 	'Price':0.0,
			# 	'Quantity':0,
			# 	'date':'00/00/000',
			# 	'total':0.0,
			# 	'status':'',
			# 	'fallback':'',
			# 	'universalCode':''
			# 	}
		}

		def accountSetup(self):
			self.name=input("Enter your full name: ")
			self.userEmail=input("Enter your Email address: ")
			self.userPassword=passCheck()
			self.userName=generateId()

		def generateId(self):
			tmp=self.name[0:2]+str(random.randrange(10,100))
			self.userName=tmp if tmp not in clientId else generateId()
			return self.userName


		def passCheck(self):
			self.userPassword=input("Chose and enter your password: ")
			verify=input("Re-enter your password: ")
			if(verify==self.userPassword):
				return self.userPassword
			else:
				print("Passwords don't match!! Try again.")
				passCheck()
				


class orderClass:	#general order class
	def __init__(self,id):
		global Id,orderCount 	#REMOVE
		self.userId=id 	#change temperory....... User id used for login
		self.pri=0		#price for each unit for buy/sell
		self.typ=''		#type of order (buy/sell)
		self.qnt=0		#quantity to be purchased/sold
		self.cmpt=0		#quantity completed at any point of time
		self.status='Pending'	#status of the order
		self.userSerial=orderCount	#serial number of order for user
		self.universalCode=hid(self.userId+str(self.userSerial))	#unique identification code for any order
		self.transactionCodes=[]	#universalCodes of all the orders which have helped complete this users order.
		orderCount+=1

	def order(self):	#order matching or addition to pending orders
		tmp=bid if self.typ=='B' else ask											#to assign tmp the dictionary which holds our specific order type
		tmp1=ask if tmp==bid else bid												#to assign tmp1 the dictionary which holds "OPPOSITE" to our specific order type
		if(self.status in ['Cancelled','Modified'] and self.pri in tmp):				#conditional to handel modified and canceled orders
				for i in tmp[self.pri]:
					if(self.universalCode==i.universalCode):								#Finding the object match from order list
						tmp[self.pri].remove(i)											#Removing the order from order list
						if(self.status=='Modified'):										#Conditional to re-insert modified order 
							self.orderMatching(tmp,tmp1)	
						if tmp[self.pri]==[]: 
							tmp.pop(self.pri)							#Remove empty list
							break
		else:
			self.orderMatching(tmp,tmp1)

		

	def orderMatching(self,tmp,tmp1):
		if self.pri in tmp1:
			for i in range(len(tmp1[self.pri])):
				zero=tmp1[self.pri][0]
				if (zero.qnt-zero.cmpt)>(self.qnt-self.cmpt):
					zero.cmpt+=self.qnt-self.cmpt
					self.cmpt=self.qnt
					self.status='Complete'
					zero.status='Partial Complete '+str(zero.qnt-zero.cmpt)+' unit/s still left'
					self.transactionCodes.append(zero.universalCode)
					zero.transactionCodes.append(self.universalCode)
					break
					#not removed obj frm list here because it has not been inserted into the list

				elif (zero.qnt-zero.cmpt)<(self.qnt-self.cmpt):
					self.cmpt+=zero.qnt-zero.cmpt
					zero.cmpt=zero.qnt
					zero.status='Complete'
					self.status='Partial Complete '+str(self.qnt-self.cmpt)+' unit/s still left'
					self.transactionCodes.append(zero.universalCode)
					zero.transactionCodes.append(self.universalCode)
					tmp1[self.pri].remove(zero)	#removed object i of bid
					if tmp1[self.pri]==[]: tmp1.pop(self.pri);break

				else:
					self.cmpt=self.qnt
					zero.cmpt=zero.qnt
					self.status='Complete'
					zero.status='Complete'
					self.transactionCodes.append(zero.universalCode)
					zero.transactionCodes.append(self.universalCode)
					tmp1[self.pri].remove(zero)
					if tmp1[self.pri]==[]: 
						tmp1.pop(self.pri)
						break

		if self.cmpt<self.qnt:
			if self.pri in tmp:
				tmp[self.pri].append(self)
			else:
				tmp.update({self.pri:[self]})	#code for matching orders and to store unmatched orders


















def testFunc():	#timepass function to take user input the format is "order type" "quantity" "price"
	test=[['B',12,13],['B',5,12],['B',4,12],['S',12,13],['S',13,12]]
	
	obj=[orderClass() for i in range(len(test))]
	a=0
	for i in obj:
		i.typ=test[a][0]
		i.pri=test[a][2]
		i.qnt=test[a][1]
		# print(i.universalCode)     #del
		i.order()
		a+=1

	obj[4].status='Modified'
	obj[4].qnt=5
	obj[4].cmpt=0
	print(obj[4].universalCode)
	obj[4].order()
	print(obj)

if __name__=="__main__":
	testFunc()
	print(bid)	#REMOVE
	print(ask)