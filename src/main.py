from pymongo import MongoClient
from flask import Flask, request
from flask_pymongo import PyMongo
import certifi
import json

ca = certifi.where()

cluster = "mongodb+srv://dio19:zsigVXU0I4jQoIZY@wazuh-server.jya46.mongodb.net/wazuh?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=ca)

app = Flask(__name__)
app.config['MONGO_URI']=cluster
mongo = PyMongo(app)

db = client.wazuh
users = db.users
tasks = db.tasks

@app.route('/tasks', methods=['GET'])
def data_tasks():
    collection = db.tasks.find()
    all_tasks = []
    for task in collection:
        data_task = {
            "user_id": task["user_id"],
            "id": task["id"],
            "title": task["title"],
             "completed": task["completed"]
        }
        all_tasks.append(data_task)
    return { "total_items": tasks.count_documents({}), "data": all_tasks }

@app.route('/tasks/<int:id>', methods=['GET'])
def data_task(id):
    task_by_id = tasks.find_one({
        "id": id
    })
    return {
            "user_id": task_by_id["user_id"],
            "id": task_by_id["id"],
            "title": task_by_id["title"],
             "completed": task_by_id["completed"]
        }

@app.route('/users', methods=['GET'])
def data_users():
    collection = db.users.find()
    all_users = []
    for user in collection:
        data_user = {
            "id": user['id'],
            "name": user['name'],
            "username": user['username'],
            "email": user['email'],
            "adress": {
                "street": user['address']['street'],
                "suite": user['address']['suite'],
                "city": user['address']['city'],
                "zipcode": user['address']['zipcode'],
                "geo": {
                    "lat": user['address']['geo']['lat'],
                    "lng": user['address']['geo']['lng'],
                }
            },
            "phone": user['phone'],
            "website": user['website'],
            "company": {
                "name": user['company']['name'],
                "catch_phrase": user['company']['catchPhrase'],
                "bs": user['company']['bs']
            },
        }
        all_users.append(data_user)
    return { "total_items": users.count_documents({}), "data": all_users }

@app.route('/users/<int:user_id>', methods=['GET'])
def data_user(user_id):
    user_by_id = users.find_one({
        "id": user_id
    })
    return {
            "id": user_by_id['id'],
            "name": user_by_id['name'],
            "username": user_by_id['username'],
            "email": user_by_id['email'],
            "adress": {
                "street": user_by_id['address']['street'],
                "suite": user_by_id['address']['suite'],
                "city": user_by_id['address']['city'],
                "zipcode": user_by_id['address']['zipcode'],
                "geo": {
                    "lat": user_by_id['address']['geo']['lat'],
                    "lng": user_by_id['address']['geo']['lng'],
                }
            },
            "phone": user_by_id['phone'],
            "website": user_by_id['website'],
            "company": {
                "name": user_by_id['company']['name'],
                "catch_phrase": user_by_id['company']['catchPhrase'],
                "bs": user_by_id['company']['bs']
            },
        }

@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def data_tasks_by_user(user_id):
    completed = request.args.get("completed", type=str)
    title = request.args.get("title", default="", type=str)
    def t_or_f(arg):
        ua = str(arg).upper()
        if 'TRUE'.startswith(ua):
            return True
        elif 'FALSE'.startswith(ua):
            return False
    tasks_by_user = []
    if completed is not None:
        tasks_by_user = tasks.find({
            "user_id": user_id,
            "completed": t_or_f(completed)
        })
    elif completed is None:
        tasks_by_user = tasks.find({
            "user_id": user_id
        })
    data = []
    for task in tasks_by_user:
        data_task = {
            "user_id": task["user_id"],
            "id": task["id"],
            "title": task["title"],
             "completed": task["completed"]
        }
        data.append(data_task)
        def iterator_func(x):
            if title in x["title"]:
                print("Exists")
                return x
            else:
                print("Does not exist")
    filtered_by_title = filter(iterator_func, data)
    print(list(filtered_by_title))
    return {
        "total_items": len(data),
        "data": data
    }

if __name__ == "__main__":
    app.run(debug=True)

# Upload data DB
# f = open("src/data/users.json")
# data = json.load(f)
# for user in data:
#     users.insert_one(user)

# f = open("src/data/tasks.json")
# data = json.load(f)
# for task in data:
#     tasks.insert_one(task)