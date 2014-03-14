import requests
import json
from pprint import pprint
url="https://api.linkedin.com/v1/people/~:(connections)"
access_token="AQX2V614SGKtvrprdXm6Gj_fAlU7bMnf-_knJc43bksaktubRYwyWMp8PIb6l3tC4UY3yVWXYgOozVk1PCE1v1qLHC0I9MItUgEEgGMH_vaQ6-JvkYCUWlM24c7YjtII1vobkGAwNSBOtKYvwYgSNDf6Ni5_GI_S8DeqJ1o94timDTU0kR8"
data_dic={"oauth2_access_token":access_token,"format":"json"}
data=requests.get(url,params=data_dic)
data=json.loads(data.text)

data=data["connections"]
data=data["values"]
id=data[0]
url="https://api.linkedin.com/v1/people/id=NDLmd1NkuG:(first-name,last-name,industry,positions,email-address,id)"
data=requests.get(url,params=data_dic)
data=json.loads(data.text)
print data