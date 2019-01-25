#!/usr/bin/python36
import os
import subprocess
#import menu_func
#import getpass
import socket
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(("192.168.43.119",1234))
s.listen(5)
session,addr=s.accept()
session.send(b"Where You Want To Execute (local/remote)")		
print("done")		
ch=session.recv(20)
option=ch.decode()	
flag=True
print(option)
if(option=='local'):
	while(flag):		
		session.send(b"""
		Press 0: To configure yum
		Press 1: To create user
		Press 2: To Delete user
		Press 3: To create file
		Press 4: To install JAVA
		Press 5: To install HADOOP
		Press 6: To Configure HADOOP
		Press 7: To Configure Mapper Reduce
		Press 8: To exit""")
		print("choice")
		ch=session.recv(20)
		x=int(ch.decode())	
		if x==0:	
			session.send(b"Please Mount the DVD")
			#print("Please Mount the DVD")	
			f=open("/etc/yum.repos.d/nit.repo","w")
			f.write("[dvd]\nbaseurl=file:///run/media/root/RHEL-7.5\ Server.x86_64\ngpgcheck=0")
			f.close()
			session.send(b"Yum Configured")
		elif x==1:
			#menu_func.create_user_local()
			print("user")
			session.send(b"Enter user name")
			#print("Enter user name")
			#name=input()
			ch=session.recv(20)
			name=ch.decode()
			user="useradd {}".format(name)
			output=subprocess.getstatusoutput(user)
			if (output[0]==0 ):
				session.send(b"User created Successfully")
				#print(" User creatsed Successfully")
			else:
				error="user Not created error: {}".format(output)
				#print(error)
				error=error.encode()
				session.send(error)
		elif x==2:
			#print("Enter user name")
			session.send(b"Enter user name")
			#name=input()
			ch=session.recv(20)
			name=ch.decode()	
			output=subprocess.getstatusoutput("userdel -r {}".format(name))
			if (output[0]==0):
				#print(" User Deleted")
				session.send(b"User Deleted")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)

		elif x==3:
			session.send(b"Enter File name")
			#file1=input()
			ch=session.recv(20)
			file1=ch.decode()
			file_name="gedit {}".format(file1)
			output=subprocess.getstatusoutput(file_name)
			if (output[0]==0):
				#print("File created")
				session.send(b"File created")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)			
		elif x==4:
			java="rpm -ivh jdk-8u171-linux-x64.rpm"
			java_home='''echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/' >> /root/.bashrc'''
			java_path='''echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin:$PATH' 	>> /root/.bashrc'''
			output=subprocess.getstatusoutput(java)
			if output[0]==0:
				a=subprocess.getoutput(java_home)
				b=subprocess.getoutput(java_path)
				#print(" Java Install And Path Set Successfully")
				session.send(b" Java Install And Path Set Successfully")
			else:
				error="Please Cheak Path of file: {}".format(output)
				error=error.encode()				
				session.send(error)
		elif x==5:
			hadoop="rpm -ivh hadoop-1.2.1-1.x86_64.rpm --force"
			output=subprocess.getstatusoutput(hadoop)
			if output[0]==0:
				#print(" Hadoop Install Successfully")
				session.send(b"Hadoop Install Successfully")
			else:
				error="Please Cheak Path of file: {}".format(output)
				error=error.encode()				
				session.send(error)
		elif x==6:
			session.send(b"""
			Hadoop Configuration	
			Press 1 For Slave
			Press 2 For Master
			Press 3 For client""")	
			#y=int(input())
			ch=session.recv(20)
			y=int(ch.decode())
			print(type(y))
			if y==1:
				#print("Enter Slave IP")
				session.send(b"Enter Slave IP")
				#slave_ip=input()
				ch=session.recv(20)
				slave_ip=ch.decode()
				file1="scp hdfs-site.xml {}:/etc/hadoop".format(slave_ip)
				output1=subprocess.getstatusoutput(file1)
				data_folder="ssh mkdir /data {}:/etc/hadoop".format(slave_ip)	
				output2=subprocess.getstatusoutput(data_folder)		
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(slave_ip)
				output3=subprocess.getstatusoutput(file2)
				if (output1[0]==0 and output3[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")
				else:
					#session.send(b"Enter user name")
					error="error: {}".format(output3)
					error=error.encode()				
					session.send(error)
			elif y==2:
				#print("Enter Master IP")
				session.send(b"Enter Master IP")
				#master_ip=input()
				ch=session.recv(20)
				master_ip=ch.decode()
				file1="scp master_hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(master_ip)
				output=subprocess.getstatusoutput(file1)
				data_folder="ssh mkdir /name {}:/etc/hadoop".format(master_ip)	
				output1=subprocess.getstatusoutput(data_folder)		
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(master_ip)
				output2=subprocess.getstatusoutput(file2)
				if (output[0]==0 and output1[0]==0 and output3[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")
				else:
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			elif y==3:
				#print("Enter Client IP")
				session.send(b"Enter Client IP")		
				#client_ip=input()	
				ch=session.recv(20)
				client_ip=ch.decode()	
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(client_ip)
				output=subprocess.getstatusoutput(file2)
				if (output[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")		
				else:
					#print("error: {}".format(output))
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			else:
				print("Invalid Input")
				session.send(b"Enter user name")
		elif x==7:
			session.send(b"""
			Mapper Reduce Configuration
			Press 1 For Job Tracker
			Press 2 For Task Tracker
			Press 3 For client""")
			#y=int(input())
			ch=session.recv(20)
			y=int(ch.decode())	
			if y==1:
				#print("Enter Job Tracker IP")
				session.send(b"Enter Job Tracker IP")				
				#jobtracker_ip=input()
				ch=session.recv(20)
				jobtracker_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(jobtracker_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					#print(error)
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)

			elif y==2:
				session.send(b"Enter Task Tracker IP")
				#tasktracker_ip=input()
				ch=session.recv(20)
				tasktracker_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(tasktracker_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					#error="error: {}".format(output)
					#print(error)	
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)	
			elif y==3:
				session.send(b"Enter Client IP")
				#client_ip=input()
				ch=session.recv(20)
				client_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(client_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			else:
				session.send(b"INVALID INPUT")		
		elif x==8:
			flag=False
			subprocess.getoutput("exit()")

elif(option=='remote'):
	#print("Enter IP")
	session.send(b"Enter Remote IP")
	ch=session.recv(20)
	ip=ch.decode()
	#ip=input()
	print(ip)
	print(type(ip))
	while(flag):
		session.send(b"""
		Press 0: To configure yum
		Press 1: To create user
		Press 2: To Delete user
		Press 3: To create file
		Press 4: To install JAVA
		Press 5: To install HADOOP
		Press 6: To Configure HADOOP
		Press 7: To Configure Mapper Reduce
		Press 8: To Launch Docker With Ansible
		Press 9: To Configure HADOOP With Ansible
		Press 10: To Exit""")
		#x=int(input())
		ch=session.recv(20)
		x=int(ch.decode())				
		if x==0:
			session.send(b"Please Mount the DVD")	
			#print("Please Mount the DVD")
			output=subprocess.getstatusoutput("ssh {}".format(ip))	
			if (output[0]==0):
				f=open("/etc/yum.repos.d/nit.repo","w")
				f.write("[dvd]\nbaseurl=file:///run/media/root/RHEL-7.5\ Server.x86_64\ngpgcheck=0")
				f.close()
				output=subprocess.getstatusoutput("exit()")
			else:
				error="error: {}".format(output)
				session.send(b"error")
				#print("ssh failed")

		elif x==1:
			session.send(b"Enter user name")
			#print("Enter user name")
			#name=input()
			ch=session.recv(20)
			name=ch.decode()
			user_ip="ssh {} useradd {}".format(ip,name)
			output=subprocess.getstatusoutput(user_ip)
			if output[0]==0:
				#print(" User created Successfully")
				session.send(b"User created Successfully")
			else:
				#print(" user Not created error: {}")
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)	
		elif x==2:
			#print("Enter user name")
			session.send(b"Enter user name")
			#name=input()
			ch=session.recv(20)
			name=ch.decode()	
			output=subprocess.getstatusoutput("userdel -r {}".format(name))
			if (output[0]==0):
				#print(" User Deleted")
				session.send(b"User Deleted")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)	
				
		elif x==3:
			#print("Enter File name")
			session.send(b"Enter File name")
			#file1=input()
			ch=session.recv(20)
			file1=ch.decode()
			file_name="ssh -X {} gedit {}".format(ip,file1)
			output=subprocess.getstatusoutput(file_name)
			if (output[0]==0):
				#print("File Created")
				session.send(b"File Created")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)	

		elif x==4:
			scp_java="scp jdk-8u171-linux-x64.rpm {}:/root".format(ip)
			java="ssh {} rpm -ivh /root/jdk-8u171-linux-x64.rpm".format(ip)
			home='''echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/' >> /root/.bashrc'''
			java_home="ssh {} {}".format(ip,home) 
			java_path='''ssh {} echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin:$PATH' >>/root/.bashrc'''.format(ip)	
			a=subprocess.getstatusoutput(scp_java)
			b=subprocess.getstatusoutput(java)
			if (b[0]==0):	
				output=subprocess.getoutput(java_home)
				#print(output)
				output=subprocess.getoutput(java_path)
				#print(" Java Install And Path Set Successfully")
				session.send(b"Java Install And Path Set Successfully")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)	

		elif x==5:
			scp_hadoop="scp hadoop-1.2.1-1.x86_64.rpm {}:/root".format(ip)
			hadoop="ssh {} rpm -ivh hadoop-1.2.1-1.x86_64.rpm --force".format(ip)
			output=subprocess.getstatusoutput(scp_hadoop)	
			output=subprocess.getstatusoutput(hadoop)
			if output[0]==0:
				#print(" Hadoop Install Successfully")
				session.send(b"Hadoop Install Successfully")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)	
				
		elif x==6:
			session.send(b"""
			Hadoop Configuration	
			Press 1 For Slave
			Press 2 For Master
			Press 3 For client""")	
			#y=int(input())
			ch=session.recv(20)
			y=ch.decode()
			if y==1:
				#print("Enter Slave IP")
				session.send(b"Enter Slave IP")
				#slave_ip=input()
				ch=session.recv(20)
				slave_ip=ch.decode()
				file1="scp hdfs-site.xml {}:/etc/hadoop".format(slave_ip)
				output1=subprocess.getstatusoutput(file1)
				data_folder="ssh mkdir /data {}:/etc/hadoop".format(slave_ip)	
				output2=subprocess.getstatusoutput(data_folder)		
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(slave_ip)
				output3=subprocess.getstatusoutput(file2)
				if (output1[0]==0 and output3[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")
				else:
					#session.send(b"Enter user name")
					error="error: {}".format(output3)
					error=error.encode()				
					session.send(error)
			elif y==2:
				#print("Enter Master IP")
				session.send(b"Enter Master IP")
				#master_ip=input()
				ch=session.recv(20)
				master_ip=ch.decode()
				file1="scp master_hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(master_ip)
				output=subprocess.getstatusoutput(file1)
				data_folder="ssh mkdir /name {}:/etc/hadoop".format(master_ip)	
				output1=subprocess.getstatusoutput(data_folder)		
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(master_ip)
				output2=subprocess.getstatusoutput(file2)
				if (output[0]==0 and output1[0]==0 and output3[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")
				else:
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			elif y==3:
				#print("Enter Client IP")
				session.send(b"Enter Client IP")		
				#client_ip=input()	
				ch=session.recv(20)
				client_ip=ch.decode()	
				file2="scp core-site.xml {}:/etc/hadoop/core-site.xml".format(client_ip)
				output=subprocess.getstatusoutput(file2)
				if (output[0]==0):
					#print("Configuration successfully")
					session.send(b"Configuration successfully")		
				else:
					#print("error: {}".format(output))
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			else:
				print("Invalid Input")
				session.send(b"Enter user name")
		elif x==7:
			session.send(b"""
			Mapper Reduce Configuration
			Press 1 For Job Tracker
			Press 2 For Task Tracker
			Press 3 For client""")
			#y=int(input())
			ch=session.recv(20)
			y=int(ch.decode())	
			if y==1:
				#print("Enter Job Tracker IP")
				session.send(b"Enter Job Tracker IP")				
				#jobtracker_ip=input()
				ch=session.recv(20)
				jobtracker_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(jobtracker_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					#print(error)
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)

			elif y==2:
				session.send(b"Enter Task Tracker IP")
				#tasktracker_ip=input()
				ch=session.recv(20)
				tasktracker_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(tasktracker_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					#error="error: {}".format(output)
					#print(error)	
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)	
			elif y==3:
				session.send(b"Enter Client IP")
				#client_ip=input()
				ch=session.recv(20)
				client_ip=ch.decode()
				file1="scp mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(client_ip)
				output=subprocess.getstatusoutput(file1)
				if output[0]==0:
					session.send(b" Successfully Configure")
				else:
					error="error: {}".format(output)
					error=error.encode()				
					session.send(error)
			else:
				session.send(b"INVALID INPUT")
				
		elif x==8:
			output=subprocess.getstatusoutput("ansible-playbook docker.yml")
			if output[0]==0:
				session.send(b"Docker Launched Successfully ")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)
		elif x==9:
			output=subprocess.getstatusoutput("ansible-playbook datanode.yml")
			output1=subprocess.getstatusoutput("ansible-playbook namenode.yml")
			if output[0]==0:
				session.send(b"Docker Launched Successfully ")
			else:
				error="error: {}".format(output)
				error=error.encode()				
				session.send(error)
		elif x==10:
			flag=False
			subprocess.getoutput("exit()")	
