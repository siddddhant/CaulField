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