
import pika
from app.parsers import *
from app import models,db
import requests
import json
from pprint import pprint
import datetime

def parse_string(s,dic):
	if(s in dic):
		return dic[s]
	else:
		return ""

def parse_dic(d,dic):
	if d in dic :
			return dic[d]
	else:
		return {}

def get_calender(s,dic):
	if s not in dic and s!="year":
		return "01"
	elif s not in dic and s=="year":
		 return "2014"
	if dic[s]<10:
		return "0"+str(dic[s])
	else:
		return str(dic[s])


def updatePersonExperienceConnection(listOfExperience,obj):
	if len(listOfExperience)==0:
		return
	for experience in listOfExperience:
		summary=parse_string("summary",experience)
		title=parse_string("title",experience)
		is_current=parse_string("isCurrent",experience)
		company_details=parse_string("company",experience)
		company_name=parse_string("name",company_details)
		company_id=parse_string("id",company_details)
		start_date=parse_dic("startDate",experience)
		end_date=parse_dic("endDate",experience)
		month_start=get_calender("month",start_date)
		year_start=get_calender("year",start_date)
		day_start=get_calender("day",start_date)
		month_end=get_calender("month",end_date)
		year_end=get_calender("year",end_date)
		day_end=get_calender("day",end_date)
		join_date=day_start+month_start+year_start
		leave_date=day_end+month_end+year_end
		join_date=datetime.datetime.strptime(join_date,"%d%m%Y").date()
		if is_current== "True":
			leave_date=""
		else:
			leave_date=datetime.datetime.strptime(leave_date,"%d%m%Y").date()

		u=models.Experience(company=company_name,company_id=company_id,position=title,location="",is_current=is_current,description=summary,start_date=join_date,end_date=leave_date,person=obj)
		db.session.add(u)



def updateConnectionData(data):
	email_address=parse_string("emailAddress",data)
	name_id=parse_string("id",data)
	name=parse_string("firstName",data)+" "+parse_string("lastName",data)
	industry=parse_string("industry",data)
	u=models.Person(access_timestamp=datetime.datetime.utcnow(),name=name,email=email_address,unique_link="",industry=industry,name_id=name_id,is_connection_source=True)
	db.session.add(u)
	updatePersonExperienceConnection(parse_string("values",parse_string("positions",data)),u)
	db.session.commit()

class recieve:

	def __init__(self):
		self.connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel=self.connection.channel()
		
		
	def queue_name(self,name):
		self.channel.queue_declare(queue=name)
		self.name=name


	def callback(self,ch,method,properties,body):
		print "Recieved "+body
		url="https://api.linkedin.com/v1/people/~:(connections)"
		data_dic={"oauth2_access_token":body,"format":"json"}
		data=requests.get(url,params=data_dic)
		data=json.loads(data.text)
		data=data["connections"]
		data=data["values"]
		print data[0]
		ids=[]
		users = models.Person.query.all()
		name_ids=[u.name_id for u in users]
		ids=[d['id'] for d in data if d["id"] not in name_ids]
		
		for id in ids:
			url="https://api.linkedin.com/v1/people/id="+id+":(first-name,last-name,industry,positions,email-address,id)"
			data=requests.get(url,params=data_dic)
			data=json.loads(data.text)
			updateConnectionData(data)
			print "Done for "+data["firstName"]
		print "Connections Added"
		

	def start_recieving(self):
		self.channel.basic_consume(self.callback,queue=self.name,no_ack=True)
		self.channel.start_consuming()

if __name__ =="__main__":
	mailer=recieve()
	mailer.queue_name("CONNECTIONS")
	mailer.start_recieving()
		
