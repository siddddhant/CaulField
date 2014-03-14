import pika

class sender:

	def __init__(self):
		self.connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel=self.connection.channel()

	def queue_name(self,name):
		self.channel.queue_declare(queue=name)
		
	def send(self,rout_key,message_body):
		self.channel.basic_publish(exchange="",routing_key=rout_key,body=message_body)

	def close(self):
		self.connection.close()
	


	
	
