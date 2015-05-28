from multiprocessing import Pool
import random

"""
	The function makes a call to random end point
"""
def f( x):
	import pycurl, json
	items = [
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php',
    'http://localhost/test.php'
	]
	rand = random.randint(0,9)
	url = 'http://localhost/test.php'
	data = json.dumps({"From": "user@example.com", "To": "receiver@example.com", "Subject": "Pycurl", "TextBody": "Some text"})
	c = pycurl.Curl()
	c.setopt(pycurl.URL, items[rand])
	c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, data)
	c.perform()
	return x

if __name__ == '__main__':
	pool = Pool(processes=100)              # start 4 worker processes
	result = pool.apply_async(f,  [500])    # evaluate "f(10)" asynchronously
	print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
	pool.map(f, range(1000))          # prints "[0, 1, 4,..., 81]"
