
response_type="code"
client_id="75invrx8tatb1y"
state="noteasyatalltoguess"
redirect_uri="http://localhost:5000/home"
client_secret="9nYblCBgazDFs5Cg"

def oauth_url():
	url="https://www.linkedin.com/uas/oauth2/authorization?"
	url+="response_type="+response_type+"&"
	url+="client_id="+client_id+"&"
	url+="scope=r_fullprofile%20r_emailaddress%20r_network&"
	url+="state="+state+"&"
	url+="redirect_uri="+redirect_uri
	return url

def get_access_token_url(auth_code):
	url="https://www.linkedin.com/uas/oauth2/accessToken"
	dic={}
	dic.update({"grant_type":"authorization_code","code":auth_code,"redirect_uri":redirect_uri,"client_id":client_id,"client_secret":client_secret})
	return (url,dic)

	
