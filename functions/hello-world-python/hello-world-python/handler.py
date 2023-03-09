import json


# echo "{"name":"John","age":30,"email":"john@example.com"}" | faas-cli invoke hello-world-python
def handle(req):
    body = json.loads(req)

    name = body["name"]
    age = body["age"]
    email = body["email"]

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps({'answer': "hello world! " + name + str(age) + email})
    }
