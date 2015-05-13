import re, urllib2

opener = urllib2.build_opener()
myurl = "http://www.brewtoad.com/recipes/"
opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]

for i in re.findall('''href=["'](.[^"']+)["']''', opener.open(myurl).read(), re.I):
	
	if i.startswith('/recipes/') :
		print i
		for ee in re.findall('''href=["'](.[^"']+)["']''', opener.open('http://www.brewtoad.com' + i).read(), re.I):
	                print ee