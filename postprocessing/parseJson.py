__author__ = 'welcome vince'

#two ways to parse Json files

import json

# use loads method (takes a string parameter)
# takes a filename and the attribute that is needed

def parseJson(filename, attribute):
    with open(filename) as f:
        data = f.read()
        jsondata = json.loads(data)

    #print data, "\n"  # shows loaded data
    print jsondata['rows']

    for file in jsondata['rows']:
        print file[attribute]

parseJson('data','title')
print "\n"

# use load method (takes a file stream)
# takes a filename and the attribute that is needed

def loadJson(filename, attribute):
    with open(filename) as f:
        jsondata = json.load(f)

    for row in jsondata['rows']:
        print row

loadJson("data", "score")