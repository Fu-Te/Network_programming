import urllib.request

url = 'https://www.google.com'

with urllib.request.urlopen(url) as f:
	html = f.read()
	print(html)