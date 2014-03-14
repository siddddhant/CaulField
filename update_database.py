import time
import datetime
from app import app
from app import db,models
import models
import requests
import re
import json
from connection_server import *
from parsers import *

def fill_partial_data(access_token,auth_token,email_address,id):
	print "Fill when connection logs in"



def updatePersonDetails(access_token,auth_token):
	users = models.Person.query.all()
	ids=[u.id for u in users ]

	data_uri="https://api.linkedin.com/v1/people/~:(first-name,last-name,industry,positions,email-address,id)"
	data_dic={"oauth2_access_token":access_token,"format":"json"}
	data=requests.get(data_uri,params=data_dic)
	data=json.loads(data.text)
	email_address=parse_string("emailAddress",data)
	name_id=parse_string("id",data)
	if name_id in ids:
		for u in users:
			if u.id==name_id:
				if u.is_connection_source==True:
					fill_partial_data(access_token,auth_token,email_address,name_id)
				else:
					return
		return


	name=parse_string("firstName",data)+" "+parse_string("lastName",data)
	industry=parse_string("industry",data)
	

	u=models.Person(access_token=access_token,auth_token=auth_token,access_timestamp=datetime.datetime.utcnow(),name=name,email=email_address,unique_link="",industry=industry,name_id=name_id,is_connection_source=False)
	db.session.add(u)
	db.session.commit()

	updatePersonExperience(parse_string("values",parse_string("positions",data)),u)
	db.session.commit()

	Sender=sender()
	Sender.queue_name("CONNECTIONS")
	Sender.send("CONNECTIONS",access_token)




def updatePersonExperience(listOfExperience,obj):
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

	

