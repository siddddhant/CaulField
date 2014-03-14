from app import db


class Person(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	unique_link=db.Column(db.String(1000),index=True)
	name=db.Column(db.String(100),index=True,unique=False)
	name_id=db.Column(db.String(100),index=True,unique=True)
	email=db.Column(db.String(100),index=True,unique=False)
	is_connection_source=db.Column(db.Boolean,index=True)
	industry=db.Column(db.String(100),index=True)
	access_token=db.Column(db.String(500),index=True,unique=False)
	auth_token=db.Column(db.String(500),index=True,unique=False)
	access_timestamp=db.Column(db.DateTime,index=True)
	
	
	#educations=db.relationship('Education',backref='Person1',lazy='dynamic')
	def __repr__(self):
		return "name is "+self.name


class Experience(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	company=db.Column(db.String(100),index=True)
	company_id=db.Column(db.String(100),index=True)
	position=db.Column(db.String(100),index=True)
	start_date=db.Column(db.Date,index=True)
	end_date=db.Column(db.Date,index=True)
	location=db.Column(db.String(100),index=True)
	description=db.Column(db.String(20000),index=True)
	is_current=db.Column(db.Boolean,index=True)
	person_id=db.Column(db.Integer,db.ForeignKey('person.id'))
	person=db.relationship('Person',backref=db.backref('experiences',lazy='dynamic'))
	
	def __repr__(self):
		return "company "+self.company

