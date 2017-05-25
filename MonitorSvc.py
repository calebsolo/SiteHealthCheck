#import libs for url methods, email methods, time, and time transformation (date)
import urllib.request
import smtplib
import time
import datetime
import pymongo

#function to get URL passed in, request url, return the status code
def get_hosts(dbserver,port):
	returnhosts = []
	connection = pymongo.MongoClient(dbserver, port)
	nodes = connection.NodeList.nodes

	try:
		cursor = nodes.find({},{"_id":0})
		for host in cursor:
			returnhosts.append(host['NodeName'])
		return returnhosts
	except:
		return "Cannot get hosts from DB."

def log_host(host,strnow,hostresp,dbserver,port):
	connection = pymongo.MongoClient(dbserver, port)
	logLine = connection.NodeList.log
	try:
		logLine.save({'NodeName':host,'ErrorTime':strnow,'ResponseCode':hostresp})
	except:
			return "Cannot log"


def get_url_status(host):
    try:
        response = urllib.request.urlopen(host) #create and issue the URL request for the url passed when the function was called
        respCode = response.getcode() #save the status code of the response to a variable
        return respCode #return the status code
    except:
        #if the host is unreachable, instead of bombing out return
        #text string of unreachable
        return "Host Unresolvable or Unreachable"

#Function to send error email if host goes down using smtplib and relaying through LIVE.COM host only to
#live.com addresses. requires a sender, recipient (receivers), the name of the host being reported on and the response code
def email_error(sender, receivers, strhost, hostresp):
    try:
        #create the body of the message with the response code and URL being tested
        message = """From: Web Check <webcheck@soileau.me>
        To: Caleb Soileau <caleb.soileau@.live.com>
        Subject: site DOWN

        """ + strhost + "responded as not functioning.  Error Code " + hostresp

        smtpObj = smtplib.SMTP('smtp.live.com',587) #form the smtp object
        smtpObj.ehlo() #issue handshake
        smtpObj.starttls() #start encryption
        smtpObj.ehlo #reissue handshake
        smtpObj.login('<something>@hotmail.com', '<PWD>') #login required to relay
        smtpObj.sendmail(sender, receivers, message) #send the email with the required parameters
        return "Successfully sent email"
    except:
        return "Email failed"

#Function to send email if host recovers and is back up, using smtplib and relaying through LIVE.COM host only to
#live.com addresses. requires a sender, recipient (receivers), the name of the host being reported on and the response code
def email_recover(sender, receivers, strhost, hostresp):
    try:
        #create the body of the message with the response code and URL being tested
        message = """From: Web Check <webcheck@soileau.me>
        To: Caleb Soileau <caleb.soileau@.live.com>
        Subject: site UP

        """ + strhost + "responded as functioning.  " + hostresp

        smtpObj = smtplib.SMTP('smtp.live.com',587) #form the smtp object
        smtpObj.ehlo() #issue handshake
        smtpObj.starttls() #start encryption
        smtpObj.ehlo #reissue handshake
        smtpObj.login(''<something>@hotmail.com', '<PWD>') #login required to relay
        smtpObj.sendmail(sender, receivers, message) #send the email with the required parameters
        return "Successfully sent email"
    except:
        return "Email failed"


#Setting variables for SMTP recipient and sender
sender = 'webcheck@soileau.me'
receivers = ['caleb.soileau@live.com']

DATABASE_HOST = 'localhost'
DATABASE_PORT = 27017


hosts = get_hosts(DATABASE_HOST,DATABASE_PORT)

#with open('in.txt','r') as incfile: #open the include file as read only
#    hosts = incfile.read().splitlines() #Remove end of line characters and save to variable.

#incfile.close() #Close the open file.

dictHost = {} #initialize the dictionary
for host in hosts: #for each host in the include file
	dictHost[host] = "" #populate the dictionary with URL and NULL


while True: #Run the below check indefinately

    #with open("log.txt", "a+") as log: #Open the log file and create if it doesn't exist.
    curdate = datetime.datetime.today() #Get the current time and date for log
    strnow = curdate.strftime("%d/%m/%Y %H:%M")

    for keyhost in dictHost.keys(): #For each host in the log file run the check for return code.
        strhost = str(keyhost)
        hostresp = str(get_url_status(strhost))
        log_host(strhost,strnow,hostresp,DATABASE_HOST,DATABASE_PORT)
        ######logic to quarentine hosts who are down and not check and alert
        if dictHost[keyhost] == "": #if the host is not reporting as previously down
            if hostresp != '200': #if it is reporting down currently
                #err_email = email_error(sender, receivers, strhost, hostresp) #send alert email
                dictHost[keyhost] = [strnow,"down",curdate] #set it's value to a down state with time in the dictionary
        if dictHost[keyhost] != "": #if the host was previously reporting down
            if hostresp != '200': #if it is currently reporting down
                errdetails = dictHost[keyhost] #get the host details form the dictionary
                errday = errdetails[2] #get the last alert time from the dictionary
                if errday < (curdate - datetime.timedelta(days=1)): #if the outage time is greater than one day from today
                    #err_email = email_error(sender, receivers, strhost, hostresp) #send alert email
                    errday = curdate #reset the alert date
                    dictHost[keyhost] = [strnow,"down",errday] #set last alert date to current date for comparison
            if hostresp == '200': #if the host was down but is now reporting up
                #recovered_email = email_recover(sender, receivers, strhost, hostresp) #send email about host recovered
                dictHost[keyhost] = "" #clear the error details
    time.sleep(900) #wait 15 min before recheck

raise SystemExit #exit the script cleanly (this will likely never run as you have to break the infinte loop, not executing this)
