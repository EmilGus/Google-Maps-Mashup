import bottle
from xml.dom import minidom
from bottle import route, run, get, post, request, response

def saveRoute(xmlobj):
	# Get all lnglat-elements and put them in a list.
	positions = xmlobj.getElementsByTagName("lnglat")

	# Extracts the Route name to use as output filename
	route_name = xmlobj.getElementsByTagName("route")
	route_name = route_name[0].getAttribute("name")

	# Iterates through the lnglat list, extracts the coordinates and adds into separate lng/lat-child elements.
	for a in positions:
		lon, lat = a.firstChild.nodeValue.split(", ")

		longitude = minidom.parseString("<lng>%s</lng>" % lon.strip('(')).documentElement
		latitude = minidom.parseString("<lat>%s</lat>" % lat.strip(')')).documentElement

		a.parentNode.appendChild(longitude)
		a.parentNode.appendChild(latitude)

	# Writes Route to XML-file.
	file = open(route_name+".xml", "w")
	xmlobj.writexml(file)
	file.close()

def getRoute(route_name):
	# Opens the filename of requested route and returns the data to requester.
	routeXML = minidom.parse(route_name+".xml")
	return(routeXML.toprettyxml())

@route('/saveRoute')
def RestfulSaveRoute():
	if request.query.route: # If route name is specified, do:
		unparsedString = request.query.route
		parsedString = minidom.parseString(unparsedString)
		saveRoute(parsedString)

@route('/getRoute')
def RestfulgetRoute():
	# Add headers to allow for Cross-origin resource sharing with Ajax.
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Content-type'] = 'application/xml'

	if request.query.route != "": # If Route name is specified, do:
		return getRoute(request.query.route)

# Start webserver and listen on port 8080 for web requests.
run(host='localhost', port=8080, debug=False)