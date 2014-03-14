from app import app
from flask import request
from flask import render_template
from flask import redirect
from flask import Response
import update_database
import re
import auth
import requests
import json







@app.route("/",methods=['GET','POST'])
@app.route("/index",methods=['GET'])
def index():
		url= auth.oauth_url()
		return render_template("index.html",url=url)
	
@app.route("/home",methods=['GET','POST'])
def home():
	return_dic=request.args
	if "code" in return_dic:
		code=return_dic['code']
	(url,dic)=auth.get_access_token_url(code)
	response=requests.post(url,data=dic)
	response_dic=json.loads(response.text)
	access_token=response_dic['access_token']
	update_database.updatePersonDetails(access_token,code)
	return render_template("home.html",data={})