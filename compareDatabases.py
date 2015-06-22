"""
To run "python compareDatabases.py <filename> <repeat count> <concurrency>"

filename - should contain all the queries you want to run with each line has a query
repeat count - Number of time each query has to be executed
concurrency - number of threads to be executed

""" 
import MySQLdb
import multiprocessing
from multiprocessing import Pool, Value, Process, Array, Lock
import sys
from sys import argv
import random
import csv, time

# thread run the queries from the file mention as many time requested in command line
def thread(lock,  val, arr, dbname = "masters"):

	#print "Started thread.... ";
	reader = val
	try:
		con = MySQLdb.connect('localhost', 'george', '', dbname)
		cursor = con.cursor( MySQLdb.cursors.DictCursor )
		con.autocommit(1)

		while val> 0:
			val = val -1

			with open( argv[1], "r") as f:
				for query in f:

					start = time.time()
					cursor.execute(query)
					lock.acquire()
					arr[0] += time.time()-start
					arr[1] = arr[1] + 1
					lock.release()
					#print "\nexecuted :"+ query
	except MySQLdb.Error, e:
		print "Error %d: %s %s" % (time.time()-start, e.args[1], query)
		sys.exit(1)
	finally:
		if con:
			con.close()


## main function starts here
if __name__ == '__main__':

	## the dbnames have the tables to run, all the queries are expected to run in all databases
	databases = ["masters", "prod_tables", "utf8mb4_tables", "barracuda_tables"]
	lock = Lock()
	for dbname in databases:
		arr =  Array('d', [0.0,0.0])
		pArr = []
		for i in range(int(argv[3])): ## threads
			p = Process(target=thread, args=( lock, int(argv[2]), arr, dbname)) ##  repeating, stats variable, dbname
			p.start()
			pArr.append(p)

		for p in pArr:
			p.join()

		print ""+"\t\t\t\t "+dbname+" \t\t\t\t\t"+ ""
		print ""+"*-"*40 + "*"
		print "*\t\tTotal Queries\t\t: " + str(arr[1]) + "\t\t\t\t*"
		print "*\t\tTime Taken(s)\t\t: " + str(round(arr[0],5)) + "\t\t\t\t*"
		print "*\t\tAvg. Time Taken(s)\t: " + str(round(arr[0]/arr[1],5)) + "\t\t\t\t*"
		print ""+"*-"*40 + "*\n"
