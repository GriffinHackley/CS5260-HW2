import boto3
import json
import sys

def readFile(bucket):
    #get all files from the bucket
    s3 = boto3.resource('s3')
    requests = s3.Bucket(bucket)
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

def writeFile(key,data, bucket):
    s3 = boto3.resource('s3')
    name = data["owner"]
    name = name.replace(" ", "-")

    path = "widgets/"+name+"/"+key

    obj = s3.Object(bucket,path)
    obj.put(Body=json.dumps(data))

    print(path)

def writeToDB():
    print("Writing to DB")

# syntax for writing to bucket:
#   {bucket name to read from} bucket {bucket name to write to}

#syntax for writing to database:
#   {bucket name to read from} db

#use command line arguments
if len(sys.argv) <= 1:
    #if no arguments
    bucket = 'usu-cs5260-hackley-requests'
    whereTo = 'usu-cs5260-hackley-web'
    storage = 1

elif sys.argv[2] == "db":
    bucket = sys.argv[1]
    storage = 0

elif sys.argv[2] == "bucket":
    bucket = sys.argv[1]
    whereTo = sys.argv[3]
    storage = 1

#read the file and return the json object and key
info = readFile(bucket)
key = info[0]
data = info[1]

#determine what kind of request the json is
if data["type"] == "create":
    if storage == 1:
        writeFile(key,data, whereTo)
    elif storage == 0:
        writeToDB()

if data["type"] == "delete":
    print("This was a delete request")

if data["type"] == "change":
    print("This was a change request")