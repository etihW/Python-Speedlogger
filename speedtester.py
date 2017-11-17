import sqlite3
import pyspeedtest
import datetime
import time
import argparse

conn = sqlite3.connect('logs.db')
logging = False
cur = conn.cursor()

#todo: add checker if the table exists, add a way to stop the script softly
#cur.execute('''CREATE TABLE log (date DATE, time TIME, ping FLOAT, speed_down FLOAT, speed_up FLOAT)''')

logging = False
def startLogging(period):
    global logging
    if not logging:
        logging = True
    loopLog(period)

def stopLogging():
    global logging
    if logging:
        logging = False

def loopLog(period):
	while logging:
		try:
			beginTest()
			time.sleep(period)
		except KeyboardInterrupt:
			print('\n\nKeyboard exception received. Exiting.')
			exit()
    

def beginTest():
    st = pyspeedtest.SpeedTest()

    print("Pinging")
    ping = st.ping()
    print("Download test")
    down = st.download()
    down = down / 1048576 #1024^2, goes from Byes to MegBytes
    print("Upload test")
    up = st.upload()
    up = up / 1048576 #Same as above

    dt = datetime.datetime.utcnow()

    date = dt.date()
    time = dt.time()

    data = [str(date), str(time), ping, down, up]
    print(data, "has been written to the database file.", sep=" ")
    cur.execute('INSERT INTO log VALUES (?,?,?,?,?)' , data)
    conn.commit() #need to commit with the connection after most executions

def printTable():
	printStr = ""
	for row in cur.execute('SELECT * FROM log'):
		for i in row:
			if type(i) is not float:
				printStr += str(i) + " "
			else:
				printStr += str("{:0.2f}".format(float(i))) + " "
		print(printStr)
		printStr = ""
def deleteLog():
    answer = input("Are you sure you want to? Type 'y' to do so.\n")
    if answer == 'y':
        cur.execute('DELETE from log')
        conn.commit()
    
def averageSpeed():
	print("\nThe average of the log is: \n")
	cur.execute('SELECT AVG(ping) FROM log')
	print("The ping is: ", cur.fetchone(), "ms")
	cur.execute('SELECT AVG(speed_down) FROM log')
	print("The download is: ", cur.fetchone(), "Mbs down")
	cur.execute('SELECT AVG(speed_up) FROM log')
	print("The upload is: ", cur.fetchone(), "Mbs up")

parser = argparse.ArgumentParser(description = "Small script that logs sppedtest results.")


parser.add_argument('-s', action="store", type = float, default = False, dest="Start", help="Start logging")
parser.add_argument('-r', action="store_true", default = False, dest="Read", help="Read the current log")
parser.add_argument('-d', action="store_true", default = False, dest="Delete", help="Delete the current log")
parser.add_argument('-a', action="store_true", default = False, dest="Avg", help="Average ping and speed of the log")

result = parser.parse_args()
if result.Start > 0:
	startLogging(result.Start)

if result.Read:
    printTable()

if result.Delete:
    deleteLog()

if result.Avg:
	averageSpeed()






















