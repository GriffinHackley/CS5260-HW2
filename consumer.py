import boto3
import json

def readFile():
    #get all files from the bucket
    s3 = boto3.resource('s3')
    requests = s3.Bucket('usu-cs5260-hackley-requests')
    allRequests = requests.objects.all()

    #get lowest keyed object from the bucket
    lowest = next(x for x in allRequests)
    for obj in allRequests:
        if lowest.key > obj.key:
            lowest = obj
    
    # get information from file into JSON format
    body = lowest.get()['Body'].read()
    return json.loads(body)
    



def createWidget():
    # takes a file and creates a widget object 
    print("Widget Created")

def writeFile():
    print("Writing File")

def writeToDB():
    print("Writing to DB")

json = readFile()
print(json)
# createWidget()
# writeFile()
# writeToDB()