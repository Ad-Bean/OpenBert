import json


# echo "{"name":"John","age":30,"email":"john@example.com"}" | faas-cli invoke hello-world-python
def handle(req):
    body = json.loads(req)

    name = body["name"]
    age = body["age"]
    email = body["email"]
    print(name)
    print(age)
    print(email)

    return "hello world" + name
