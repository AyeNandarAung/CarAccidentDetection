import Tkinter as tk
import RPi.GPIO as GPIO
import smbus
import time
import datetime
import sys
import urllib
#import urllib.request
import json
from urllib import urlopen
import serial
import string
import pynmea2
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from retrievegyro import readRotation
import tkMessageBox
from InsertDB import InsertData
from DBupdate import UpdateData
import mysql.connector
from mysql.connector import Error
from twilio.rest import Client
from retrievedistance import distance

class MainCarAccidentDetectionApp:
    def __init__(self):
	self.lat=0
	self.lng=0
        self.root=tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("850x650")
        self.startpage_gui()
        self.root.mainloop()
        
    def startpage_gui(self):
        self.photo = tk.PhotoImage(file="Images/caraccident128.png")
        self.logo  = tk.Label(self.root,image=self.photo)
        self.logo.grid(row=0,column=0,pady=(90,0))
        
        self.photo1 = tk.PhotoImage(file="Images/emservice128.png")
        self.logo1  = tk.Label(self.root,image=self.photo1)
        self.logo1.grid(row=0,column=1,pady=(90,0))

        self.title = tk.Label(self.root,text="Car Accident Detection Alert!",fg="blue4",font=("Candara 30 bold"))
        self.title.grid(row=1,column=0,columnspan=2,padx=(100),pady=(30,50))
        self.start_button = tk.Button(self.root, text="START",font=("Candara 12 bold"),command=self.showdatapage,bg="lime green",width=17)
        self.start_button.grid(row=2,column=0,columnspan=2)
        #new..

        self.addphoto = tk.PhotoImage(file = "Images/emservice1.png") 
  
        self.addphoto = self.addphoto.subsample(3,3) 
         

        self.add_button = tk.Button(self.root,text="Emergency Services!",fg="blue4",font=("Candara 10 bold"),image=self.addphoto,compound=tk.TOP, highlightthickness = 0, bd = 0,command=self.showall,width=17)
        self.add_button.grid(row=3,column=0,columnspan=2,pady=(10,30))
        self.add_button.config(height=100,width=300)
        
        self.supervisor = tk.Label(self.root,text="Supervised By",fg="blue4",font=("Candara 12 bold"))
        self.supervisor.grid(row=4,column=0,pady=(0,0))        
        self.supervisorname = tk.Label(self.root,text="U Myint San and Daw Khin Thuzar",fg="blue4",font=("Candara 12 bold"))
        self.supervisorname.grid(row=5,column=0,pady=(0,0))
               
        self.presenter = tk.Label(self.root,text="Presented By",fg="blue4",font=("Candara 12 bold"))
        self.presenter.grid(row=4,column=1,pady=(0,0),)        
        self.presentername = tk.Label(self.root,text="Aye Nandar Aung(6IST-12)",fg="blue4",font=("Candara 12 bold"))
        self.presentername.grid(row=5,column=1,pady=(0,0))
        

        
    def showdatapage_gui(self):
        self.labely=tk.Label(self.root,text="Y-Acceleration",fg="blue4",font=("Candara 19 bold"))
        self.labely.grid(row=0,column=0,padx=(20),pady=(60,20))
        self.labelz=tk.Label(self.root,text="Z-Acceleration",fg="blue4",font=("Candara 19 bold"))
        self.labelz.grid(row=0,column=1,padx=(50),pady=(60,20))
        self.labelvibration=tk.Label(self.root,text="Vibration",fg="blue4",font=("Candara 19 bold"))
        self.labelvibration.grid(row=0,column=2,padx=(40),pady=(60,20))
        self.labelrotation=tk.Label(self.root,text="Rotation",fg="blue4",font=("Candara 19 bold"))
        self.labelrotation.grid(row=0,column=3,padx=(40),pady=(60,20))



        self.labelydata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelydata.grid(row=1,column=0,padx=(20),pady=(0,50))
        self.labelzdata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelzdata.grid(row=1,column=1,padx=(50),pady=(0,50))
        self.labelvibrationdata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelvibrationdata.grid(row=1,column=2,padx=(40),pady=(0,50))
	self.labelrotationdata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelrotationdata.grid(row=1,column=3,padx=(40),pady=(0,50))


        self.labelcarstate=tk.Label(self.root,text="Car Status",fg="blue4",font=("Candara 19 bold"))
        self.labelcarstate.grid(row=2,column=0,padx=(20),pady=(0,60))
        #self.photo = tk.PhotoImage(file="Images/car128.png")
        #self.labelcarstatus= tk.Label(self.root,image=self.photo)
        #self.labelcarstatus.grid(row=2,column=1,padx=(20),pady=(0,50))
        self.labelcarstatedata=tk.Label(self.root,text="None",fg="blue4",font=("Candara 19 bold"))
        self.labelcarstatedata.grid(row=2,column=1,padx=(20),pady=(0,60))

        self.labelocation=tk.Label(self.root,text="Current Location",fg="blue4",font=("Candara 19 bold"))
        self.labelocation.grid(row=3,column=0,padx=(20),pady=(0,50))
        self.labelocationlat=tk.Label(self.root,text="Lattitude",fg="blue4",font=("Candara 19 bold"))
        self.labelocationlat.grid(row=3,column=1,padx=(20),pady=(0,50))
        self.labelocationlong=tk.Label(self.root,text="Longitude",fg="blue4",font=("Candara 19 bold"))
        self.labelocationlong.grid(row=3,column=2,padx=(20),pady=(0,50))

        self.photo = tk.PhotoImage(file="Images/location64.png")
        self.labelcarstatus= tk.Label(self.root,image=self.photo)
        self.labelcarstatus.grid(row=4,column=0,padx=(20),pady=(0,30))
        self.labelocationlatdata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelocationlatdata.grid(row=4,column=1,padx=(20),pady=(0,30))
        self.labelocationlongdata=tk.Label(self.root,text="0",fg="blue4",font=("Candara 19 bold"))
        self.labelocationlongdata.grid(row=4,column=2,padx=(20),pady=(0,30))
	

        self.stop_button = tk.Button(self.root, text="STOP",font=("Candara 12 bold"),command=self.stoppage_gui,bg="orange",width=17)
        self.stop_button.grid(row=5,column=0,columnspan=3)
        WRITE_API = "R2VX50RNBMM8PJY7"
        BASE_URL="https://api.thingspeak.com/update?api_key={}".format(WRITE_API)
        while True:            
                carstate="None"
                DateandTime=datetime.datetime.now()
		x,y,z=self.readAccelerometer()
		carvibration=self.readVibration()
		carrotation=readRotation()
		lat,long=self.readgps()
                self.labelydata["text"]=y
                self.labelzdata["text"]=z
		self.labelvibrationdata["text"]=carvibration
		self.labelrotationdata["text"]=carrotation
		carstate=self.isAccident(y,z,carvibration,carrotation)
		#print(carstate)		
                thingspeakHttp=BASE_URL+"&field1={}&field2={}&field3={}field4={}&field5={}&field6={}&field7={}&field8={}".format(y,z,carvibration,carrotation,carstate,lat,long,DateandTime)
                #print(thingspeakHttp)
                conn=urlopen(thingspeakHttp)
                #print("Response:{}".format(conn.read()))
                conn.close()
                
		if (carstate=="Accident"):
                        lat,long=self.readgps()
			#if(lat!=0.0 and long!=0.0):
                        self.labelcarstatedata["text"]="Accident"
                        self.labelcarstatedata.config(fg='Maroon')
                        
                        if(lat!=0.0 and long!=0.0):
                            self.labelocationlatdata["text"]=lat
                            self.labelocationlongdata["text"]=long                        
                            self.sendMessage(lat,long)
                        else:
                            lat,long=self.readgps()
                            continue
                            #self.labelocationlatdata["text"]=lat
                            #self.labelocationlongdata["text"]=long                        
                            #self.sendMessage(lat,long)
                            

		else:
			
			self.labelcarstatedata["text"]="Normal"
			self.labelcarstatedata.config(fg='DarkGreen')
			self.labelocationlatdata["text"]='0'
			self.labelocationlongdata["text"]='0'
		
		self.root.update()
		time.sleep(1)
#new
    def showall(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("1200x650")
        self.showalldatapage_gui()
        self.root.mainloop()
   
#new        
    def showalldatapage_gui(self):
        
        self.photo = tk.PhotoImage(file="Images/center.png")
        self.photo = self.photo.subsample(3,3) 
        self.logo  = tk.Label(self.root,image=self.photo)
        self.logo.grid(row=0,column=0,padx=(50,0),pady=(5,0))

        self.labelall= tk.Label(self.root,text="All Emergency Services in the system",fg="blue4",font=("Candara 12 bold"))
        self.labelall.grid(row=0,column=1,columnspan=2,pady=(5,0))
        
        #self.photo1 = tk.PhotoImage(file="Images/center.png"),padx=(30,0),padx=(50,0)
        #self.photo1 = self.photo1.subsample(3,3) 
        #self.logo1  = tk.Label(self.root,image=self.photo1)
        #self.logo1.grid(row=0,column=0,padx=(250,0),pady=(20,0))


        #self.frame=tk.Frame(self.root)
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='thesisdb',
                                         user='root',
                                         password='root')
            sql_select_Query = "select * from emservice"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            #print("Total number of rows in Laptop is: ", cursor.rowcount)
            #print("\nPrinting each EMService record")
            btnid=0
            i=2
            b=0
            for row in records:                
                for j in range(len(row)):
                    self.e = tk.Entry(self.root, width=13,background="white",font=("Candara 12 bold "))                
                    self.e.grid(row=i, column=j,padx=(0,0)) 
                    self.e.insert(tk.END,row[j])
                    self.e.config(state='read')
                    self.e.config(fg='black')
                    #self.e.config(bg='white')
                    #self.e.config(state='disabled')
                    #print(row[0])
                    btnid =row[0]
                    
               
                #self.btn=tk.Button(self.root,text="ok")
                #self.btn.grid(row=i, column=j) 
                #self.btn.insert(tk.END,multi[j])
                
                self.btne=tk.Button(self.root,text="Edit",bg="green",fg="white",command=lambda k= btnid : self.update(k))
                self.btne.grid(row=i, column=j+1)
                self.btnd=tk.Button(self.root,text="Delete",bg="red",fg="white",command=lambda k=btnid:self.delete(k))
                self.btnd.grid(row=i, column=j+2,pady=(0,5))
                i=i+1
                
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                #print("MySQL connection is closed")

          
        #multi_array = [[1, 2,3,4],[6, 7,3,4]]

        #i=2
        self.Lid = tk.Label(self.root,text="No.", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.Lid.grid(row=1, column=0,sticky='w',pady=(30))

        self.L = tk.Label(self.root,text="Name", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L.grid(row=1, column=1,sticky='w',pady=(30))
        self.L1 = tk.Label(self.root,text="Phone", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L1.grid(row=1, column=2,sticky='w',pady=(30))
        self.L4 = tk.Label(self.root,text="Latitude", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L4.grid(row=1, column=3,sticky='w',pady=(30))
        self.L5 = tk.Label(self.root,text="Latitude", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L5.grid(row=1, column=4,sticky='w',pady=(30))
        self.L2 = tk.Label(self.root,text="To Edit", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L2.grid(row=1, column=5,sticky='w',pady=(30))
        self.L3 = tk.Label(self.root,text="To Delete", width=10, fg='blue4',font=("Candara 12 bold"))    
        self.L3.grid(row=1, column=6,sticky='w',pady=(30)) 
        
        #for multi in multi_array: 
            #for j in range(len(multi)):
                #self.e = tk.Entry(self.root, width=10, fg='blue4',font=("Candara 13 bold"))                
                #self.e.grid(row=i, column=j,padx=(0,0)) 
                #self.e.insert(tk.END,multi[j])
                #self.e.config(state='disabled')
                
            #self.btne=tk.Button(self.root,text="Edit",bg="green",fg="white",command=self.update)
            #self.btne.grid(row=i, column=j+1)
            #self.btnd=tk.Button(self.root,text="Delete",bg="red",fg="white")
            #self.btnd.grid(row=i, column=j+2,pady=(0,5))

            #i=i+1
        


        self.addphoto = tk.PhotoImage(file = "Images/plus128.png")   
        self.addphoto = self.addphoto.subsample(3,3)       
        self.add_button = tk.Button(self.root,text="Add Services!",fg="blue4",font=("Candara 12 bold"),image=self.addphoto,compound=tk.TOP,command=self.insert, highlightthickness = 0, bd = 0,width=17)
        self.add_button.grid(row=0,column=5,pady=(0,30))
        self.add_button.config(height=100,width=100)
        
        
        self.backphoto = tk.PhotoImage(file = "Images/back.png")   
        self.backphoto = self.backphoto.subsample(3,3)          
        self.back_button = tk.Button(self.root,text="Back",fg="blue4",font=("Candara 12 bold"),image=self.backphoto,compound=tk.TOP,command=self.stoppage_gui, highlightthickness = 0, bd = 0,width=17)
        self.back_button.grid(row=0,column=6,pady=(0,30))
        self.back_button.config(height=100,width=100)

#new       

    def insert(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("900x650")
        self.insertdatapage_gui()
        self.root.mainloop()
    def delete(self,btnid):
        try:
            connection = mysql.connector.connect(host='localhost',
                                             database='thesisdb',
                                             user='root',
                                             password='root')
            cursor = connection.cursor()
            sql_delete_query = """Delete from emservice where Id = %s"""
            
            cursor.execute(sql_delete_query, (btnid,))
            connection.commit()
            #print("Record Delete successfully ")
        except mysql.connector.Error as error:
            print("Failed to delete record to database: {}".format(error))
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                #print("MySQL connection is closed")
        
        #print(btnid)
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("900x650")
        self.showalldatapage_gui()
        self.root.mainloop()

#new        
        
    def insertdatapage_gui(self):
        self.photo = tk.PhotoImage(file="Images/ambulance.png")
        
        self.logo  = tk.Label(self.root,image=self.photo)
        self.logo.grid(row=0,column=0,columnspan=2,padx=(100,0),pady=(20,0))
        
        self.photo1 = tk.PhotoImage(file="Images/hospital.png")
        self.photo1 = self.photo1.subsample(4,4) 
        self.logo1  = tk.Label(self.root,image=self.photo1)
        self.logo1.grid(row=0,column=1,columnspan=2,padx=(250,0),pady=(20,0))

        self.labelname=tk.Label(self.root,text="Service Name",fg="blue4",font=("Candara 12 bold"))
        self.labelname.grid(row=1,column=0,pady=(70,100),padx=(50,0))
        
        self.labelnameentry=tk.Entry(self.root)
        self.labelnameentry.grid(row=1,column=1,padx=(0),pady=(70,100))
        
        self.labelphone=tk.Label(self.root,text="Phone Number",fg="blue4",font=("Candara 12 bold"))
        self.labelphone.grid(row=1,column=2,pady=(70,100))        

        self.labelphoneentry=tk.Entry(self.root)
        self.labelphoneentry.grid(row=1,column=3,pady=(70,100))

        self.labelLat=tk.Label(self.root,text="Latitude",fg="blue4",font=("Candara 12 bold"))
        self.labelLat.grid(row=2,column=0,pady=(0,50),padx=(50,0))
        
        self.labelLatentry=tk.Entry(self.root)
        self.labelLatentry.grid(row=2,column=1,padx=(0),pady=(0,50))
        
        self.labelLong=tk.Label(self.root,text="Longitude",fg="blue4",font=("Candara 12 bold"))
        self.labelLong.grid(row=2,column=2,pady=(0,50))        

        self.labelLongentry=tk.Entry(self.root)
        self.labelLongentry.grid(row=2,column=3,pady=(0,50))
        
        
        self.register_button = tk.Button(self.root, text="Register!",font=("Candara 12 bold"),fg="blue4",command=self.InsertDB,bg="lime green",width=15)
        self.register_button.grid(row=3,column=0,columnspan=4)
        
    def InsertDB(self):
        servicename = self.labelnameentry.get()
        phonenumber = self.labelphoneentry.get()
        lat = float(self.labelLatentry.get())
        long = float(self.labelLongentry.get())
        #print(servicename,phonenumber,lat,long)
        status = InsertData(servicename,phonenumber,lat,long)
        #print (status)
        tkMessageBox.showinfo("Information",status)
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("900x650")
        self.startpage_gui()
        self.root.mainloop()           

#new       

    def update(self,btnid):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("900x650")
        
        self.updatedatapage_gui(btnid)
        self.root.mainloop()

#new        
        
    def updatedatapage_gui(self,btnid):
        self.photo = tk.PhotoImage(file="Images/ambulance.png")
        
        self.logo  = tk.Label(self.root,image=self.photo)
        self.logo.grid(row=0,column=0,columnspan=2,padx=(100,0),pady=(20,0))
        
        self.photo1 = tk.PhotoImage(file="Images/hospital.png")
        self.photo1 = self.photo1.subsample(4,4) 
        self.logo1  = tk.Label(self.root,image=self.photo1)
        self.logo1.grid(row=0,column=1,columnspan=2,padx=(250,0),pady=(20,0))

        self.labelname=tk.Label(self.root,text="Service Name",fg="blue4",font=("Candara 12 bold"))
        self.labelname.grid(row=1,column=0,pady=(70,100),padx=(50,0))
        
        self.labelnameentry=tk.Entry(self.root)
        self.labelnameentry.grid(row=1,column=1,padx=(0),pady=(70,100))
        
        self.labelphone=tk.Label(self.root,text="Phone Number",fg="blue4",font=("Candara 12 bold"))
        self.labelphone.grid(row=1,column=2,pady=(70,100))        

        self.labelphoneentry=tk.Entry(self.root)
        self.labelphoneentry.grid(row=1,column=3,pady=(70,100))

        self.labelLat=tk.Label(self.root,text="Latitude",fg="blue4",font=("Candara 12 bold"))
        self.labelLat.grid(row=2,column=0,pady=(0,50),padx=(50,0))
        
        self.labelLatentry=tk.Entry(self.root)
        self.labelLatentry.grid(row=2,column=1,padx=(0),pady=(0,50))
        
        self.labelLong=tk.Label(self.root,text="Longitude",fg="blue4",font=("Candara 12 bold"))
        self.labelLong.grid(row=2,column=2,pady=(0,50))        

        self.labelLongentry=tk.Entry(self.root)
        self.labelLongentry.grid(row=2,column=3,pady=(0,50))
        
        
        self.editsave_button = tk.Button(self.root, text="Save",font=("Candara 12 bold"),fg="blue4",command=lambda k= btnid : self.successupdate(k),bg="lime green",width=15)
        self.editsave_button.grid(row=3,column=0,columnspan=4)
        #print(btnid)
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='thesisdb',
                                         user='root',
                                         password='root')
            sql_select_Query = "select ServiceName,PhoneNumber,Latitude,Longitude from emservice where Id = %s"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query,(btnid,))
            records = cursor.fetchall()
            print("Total number of rows in Laptop is: ", cursor.rowcount)
            print("\nPrinting each EMService record")
           
            for row in records:
                self.labelnameentry.insert(0,row[0])
                self.labelphoneentry.insert(0,row[1])
                self.labelLatentry.insert(0,row[2])
                self.labelLongentry.insert(0,row[3])
                
 
                
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")



    def successupdate(self,btnid):
        servicename = self.labelnameentry.get()
        phonenumber = self.labelphoneentry.get()
        lat = float(self.labelLatentry.get())
        long = float(self.labelLongentry.get())
        #print(servicename,phonenumber,lat,long)
        status = UpdateData(btnid,servicename,phonenumber,lat,long)
        tkMessageBox.showinfo("Information",status)
        self.root.destroy()
        self.root = tk.Tk()
        self.root.geometry("1100x650")
        self.root.title("Car Accident Detection")
        #self.root.geometry("650x500")
        self.showalldatapage_gui()
        self.root.mainloop()        


    def showdatapage(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("1000x650")
        self.showdatapage_gui()
        self.root.mainloop()
        
    def stoppage_gui(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Car Accident Detection")
        self.root.geometry("900x650")
        self.startpage_gui()
        self.root.mainloop()
        
    def readAccelerometer(self):
        bus= smbus.SMBus(1)
        time.sleep(1)
        bus.write_byte_data(0x53,0x2C,0x0A)
        bus.write_byte_data(0x53,0x2D,0x08)
        bus.write_byte_data(0x53,0x31,0x08)
        
        data0=bus.read_byte_data(0x53,0x32)
	data1=bus.read_byte_data(0x53,0x33)
	xAccl=((data1 & 0x03)*256)+data0
	if xAccl > 511:
		xAccl -=1024

	data0=bus.read_byte_data(0x53,0x34)
	data1=bus.read_byte_data(0x53,0x35)
	yAccl =((data1 & 0x03)*256)+data0
	if yAccl > 511:
        	yAccl -=1024
            
	data0=bus.read_byte_data(0x53,0x36)
	data1=bus.read_byte_data(0x53,0x37)
	zAccl = ((data1 & 0x03)*256)+data0
	if zAccl > 511:
        	zAccl -=1024

        #print "Acceleration in X-Axis: %d" %xAccl
	#print "Acceleration in Y-Axis: %d" %yAccl
	#print "Acceleration in Z-Axis: %d" %zAccl
	#time.sleep(5)
	return xAccl,yAccl,zAccl;

    def readVibration(self):
	channel = 17
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(channel,GPIO.IN)
	if GPIO.input(channel):
                vibration=1
                #print (vibration)
        else:
                vibration=0
                #print(vibration)
	return vibration;

    def sendMessage(self,lat,lon):
        distancekm={}
        accidentLocation = lat,lon
        print("Accident Location is",accidentLocation)
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='thesisdb',
                                         user='root',
                                         password='root')
            sql_select_Query = "select Latitude,Longitude from emservice"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            print("Total number of rows in Laptop is: ", cursor.rowcount)
            print("\nPrinting each EMService record")
           
            for row in records:
                emserviceLocation=row[0],row[1]
                distancekm[emserviceLocation] = round(distance(accidentLocation,emserviceLocation),0)         
            #print(distancekm)
            #print(min(distancekm))           
            #print(distancekm.values())
            #closerlat,closerlng=min(distancekm)
            #print(type(distancekm[closerlat,closerlng]))
            #print(distancekm[lat,lng])
            minvalue=0
            for keys in distancekm:
                distancekm[keys]=int(distancekm[keys])
            print(distancekm)            
            closestdist=min(distancekm.values())
            for key, value in distancekm.items():
                if closestdist == value:
                    closerlat,closerlng=key
                
            print(closerlat,closerlng)
            
 
                            
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        
    
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='thesisdb',
                                         user='root',
                                         password='root')
            sql_select_Query = "select PhoneNumber from emservice where Latitude LIKE %s and Longitude LIKE %s"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query,(closerlat,closerlng,))
            records = cursor.fetchall()
            #print("Total number of rows in Laptop is: ", cursor.rowcount)
            #print("\nPrinting each EMService record")
            emcenter =""
            for row in records:
                emphone = row[0]
            #receive="+959963295100"
            lst=list(emphone)
            lst[0]='+95'
            emservicephone=''
            for i in lst:
                emservicephone+=i
            receive = emservicephone
            print(receive)
            response = urllib.urlopen('https://api.thingspeak.com/channels/1083833/feeds.json?results=2')
            datastring = response.read().decode('utf-8')
            json_obj= json.loads(datastring)
            #print(json_obj['feeds'])
            for i in json_obj['feeds']:
                data_dict=i
            print(data_dict["field8"])
            Date_Time=data_dict["field8"]
            account_sid="AC7fc401d8ea852385ee3dc9965de26566"
            auth_token="73400598cab1669cc6c3537adf7f890e"
            client=Client(account_sid,auth_token)
            message=client.api.account.messages.create(to=receive,from_="+17866613092",body="Car Accident is occured at the location "+str(closerlat)+" and "+str(closerlng)+"  Date and Time is "+Date_Time)
            print("Send message successfully! to",closerlat,closerlng,Date_Time)
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        

 

    def readgps(self):
        port="/dev/ttyS0"
	ser=serial.Serial(port,baudrate=9600,timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	
	if newdata[0:6]=="$GPRMC":
		#print("hi")
		newmsg=pynmea2.parse(newdata)
		self.lat=round(newmsg.latitude,4)
		self.lng=round(newmsg.longitude,4)
		#gps = "Latitude = " + str(lat)  + " and Longitude = " + str(lng)
		#print(gps)
		#lat=(lat)
	#time.sleep(5)       
	return self.lat,self.lng;
    
    def isAccident(self,ydata,zdata,vdata,rdata):
         state="none"
         Y = ctrl.Antecedent(np.arange(-250, 300,1), 'Y')
         Y['LargeNegative'] = fuzz.trapmf(Y.universe, [-250,-250,-200,-100])
         Y['Small'] = fuzz.trapmf(Y.universe, [-200,-100,100,250])
         Y['LargePositive'] = fuzz.trapmf(Y.universe, [100,250,300,300])

         Z = ctrl.Antecedent(np.arange(-277,240,1), 'Z')
         Z['LargeNegative'] = fuzz.trapmf(Z.universe, [-277,-277,-200,-100])
         Z['Small'] = fuzz.trapmf(Z.universe, [-200,-100,100,160])
         Z['LargePositive'] = fuzz.trapmf(Z.universe, [100,160,240 ,240])

	 Vibration= ctrl.Antecedent(np.arange(0, 1,0.1), 'Vibration')
	 Vibration['Low'] = fuzz.trimf(Vibration.universe, [0,0,0.5])
	 Vibration['High'] = fuzz.trimf(Vibration.universe, [0.5,1,1])
	
	 Rotation= ctrl.Antecedent(np.arange(-88, 88,1), 'Rotation')
	 Rotation['NegativeHighDegree'] = fuzz.trapmf(Rotation.universe, [-88,-88,-40,-30])
	 Rotation['SmallDegree'] = fuzz.trapmf(Rotation.universe, [-40,-30,30,40])
	 Rotation['PositiveHighDegree'] = fuzz.trapmf(Rotation.universe, [30,40,88,88])

         Car_Status= ctrl.Consequent(np.arange(0, 100, 1), 'Car_Status')
         Car_Status['Normal'] = fuzz.trapmf(Car_Status.universe, [0,0,30,70])
         Car_Status['Accident'] = fuzz.trapmf(Car_Status.universe, [30,70,100,100])

	 
	 rule1 = ctrl.Rule(Z['LargeNegative'],Car_Status['Accident'])
	 rule2 = ctrl.Rule(Y['LargeNegative']&Z['LargeNegative']&Vibration['Low']&Rotation['NegativeHighDegree'], Car_Status['Accident'])
	 rule3 = ctrl.Rule(Y['LargeNegative']&Z['Small']&Vibration['Low']&Rotation['NegativeHighDegree'], Car_Status['Accident'])
 	 rule4 = ctrl.Rule(Y['LargeNegative']&Z['LargeNegative']&Vibration['High']&Rotation['NegativeHighDegree'], Car_Status['Accident'])
	 rule5 = ctrl.Rule(Y['LargeNegative']&Z['Small']&Vibration['High']&Rotation['NegativeHighDegree'], Car_Status['Accident'])
	 rule6 = ctrl.Rule(Y['Small']&Z['LargePositive']&Vibration['Low']&Rotation['SmallDegree'], Car_Status['Normal'])
	 rule7 = ctrl.Rule(Y['Small']&Z['LargeNegative']&Vibration['Low']&Rotation['SmallDegree'], Car_Status['Accident'])
	 rule8 = ctrl.Rule(Y['Small']&Z['Small']&Vibration['Low']&Rotation['SmallDegree'], Car_Status['Normal'])
	 rule9 = ctrl.Rule(Y['Small']&Z['LargePositive']&Vibration['High']&Rotation['SmallDegree'], Car_Status['Accident'])
 	 rule10 = ctrl.Rule(Y['Small']&Z['LargeNegative']&Vibration['High']&Rotation['SmallDegree'], Car_Status['Accident'])
	 rule11 = ctrl.Rule(Y['Small']&Z['Small']&Vibration['High']&Rotation['SmallDegree'], Car_Status['Accident'])
	 rule12 = ctrl.Rule(Y['LargePositive']&Z['LargeNegative']&Vibration['Low']&Rotation['PositiveHighDegree'], Car_Status['Accident'])
	 rule13 = ctrl.Rule(Y['LargePositive']&Z['Small']&Vibration['Low']&Rotation['PositiveHighDegree'], Car_Status['Accident'])
	 rule14 = ctrl.Rule(Y['LargePositive']&Z['LargeNegative']&Vibration['High']&Rotation['PositiveHighDegree'], Car_Status['Accident'])
	 rule15 = ctrl.Rule(Y['LargePositive']&Z['Small']&Vibration['High']&Rotation['PositiveHighDegree'], Car_Status['Accident'])
	 rule16 = ctrl.Rule(Y['Small']&Z['LargePositive']&Vibration['High']&Rotation['PositiveHighDegree'], Car_Status['Accident'])
	 #rule17 = ctrl.Rule(Y['LargePositive']&Z['Small']&Vibration['High']&Rotation['Small'], Car_Status['Accident'])
	 #rule17 = ctrl.Rule(Y['LargePositive']&Z['Small']&Vibration['High']&Rotation['Small'], Car_Status['Accident'])
 

	 Car_Status_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,rule14,rule15,rule16])

         Car_Status_Decision = ctrl.ControlSystemSimulation(Car_Status_ctrl)
         Car_Status_Decision.input['Y']=ydata
         Car_Status_Decision.input['Z']=zdata
	 Car_Status_Decision.input['Vibration']=vdata
	 Car_Status_Decision.input['Rotation']=rdata

         Car_Status_Decision.compute()
 	 COG=Car_Status_Decision.output['Car_Status']
        #print (Car_Status_Decision.output['Car_Status'])
        #rule1.view()
         if (COG>50):
         	#print('Accident')
         	state='Accident'
		#print(state) 
        
         else:
         	#print('Normal')
         	state='Normal'              
	 return state;



if __name__ == '__main__':
        MainCarAccidentDetectionApp()        
    
