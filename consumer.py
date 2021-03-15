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

    #delete objcet from bucket
    key = lowest.key
    # lowest.delete()

    return (key,json.loads(body))

def writeFile(key,data):
    # s3 = boto3.client('s3')
    s3 = boto3.resource('s3')
    name = data["owner"]
    name = name.replace(" ", "-")

    path = "widgets/"+name+"/"+key

    obj = s3.Object('usu-cs5260-hackley-web',path)
    obj.put(Body=json.dumps(data))

    print(path)

def writeToDB():
    print("Writing to DB")

#read the file and return the json object
info = readFile()
key = info[0]
data = info[1]

#determine what kind of request the json is
if data["type"] == "create":
    writeFile(key,data)

if data["type"] == "delete":
    print("This was a delete request")

if data["type"] == "change":
    print("This was a change request")


# writeToDB()