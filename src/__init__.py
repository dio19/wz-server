from pymongo import MongoClient
from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
from flask_cors import CORS
import certifi

def create_app():
    ca = certifi.where()

    cluster = "mongodb+srv://dio19:zsigVXU0I4jQoIZY@wazuh-server.jya46.mongodb.net/wazuh?retryWrites=true&w=majority"
    client = MongoClient(cluster, tlsCAFile=ca)

    app = Flask(__name__)
    app.config['MONGO_URI']=cluster
    CORS(app)
    mongo = PyMongo(app)

    try:
        db = client.wazuh
        users = db.users
        tasks = db.tasks
    except Exception as e:
        print('Cannot connect to DB: ', e)

    @app.route('/tasks', methods=['GET'])
    def data_tasks():
        collection = db.tasks.find()
        if collection is not None:
            all_tasks = []
            for task in collection:
                data_task = {
                    "user_id": task["user_id"],
                    "id": task["id"],
                    "title": task["title"],
                    "completed": task["completed"]
                }
                all_tasks.append(data_task)
        else:
            return jsonify({"error": "An error occurred with tasks collection"}), 503
        try:
            return { "total_items": tasks.count_documents({}), "data": all_tasks }
        except Exception as e:
            return jsonify({"An exception occurred": e})

    @app.route('/tasks/<int:id>', methods=['GET'])
    def data_task(id):
        task_by_id = tasks.find_one({
            "id": id
        })
        if task_by_id is None:
            return abort(422, description="Please enter a valid task ID")
        try:
            return {
                "user_id": task_by_id["user_id"],
                "id": task_by_id["id"],
                "title": task_by_id["title"],
                "completed": task_by_id["completed"]
            }
        except Exception as e:
            return jsonify({"An exception occurred": e})

    @app.route('/users', methods=['GET'])
    def data_users():
        collection = db.users.find()
        if collection is not None:
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
        else:
            return jsonify({"error": "An error occurred with users collection"}), 503
        try:
            return { "total_items": users.count_documents({}), "data": all_users }
        except Exception as e:
            return jsonify({"An exception occurred": e})

    @app.route('/users/<int:user_id>', methods=['GET'])
    def data_user(user_id):
        user_by_id = users.find_one({
            "id": user_id
        })
        if user_by_id is None:
            return abort(422, description="Please enter a valid user ID")
        try:
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
        except Exception as e:
            return jsonify({"An exception occurred": e})

    @app.route('/users/<int:user_id>/tasks', methods=['GET'])
    def data_tasks_by_user(user_id):
        user_by_id = users.find_one({
            "id": user_id
        })
        if user_by_id is None:
            return abort(422, description="Please enter a valid user ID")
        completed = request.args.get("completed", type=str)
        def t_or_f(arg):
            ua = str(arg).upper()
            if 'TRUE'.startswith(ua):
                return True
            elif 'FALSE'.startswith(ua):
                return False
            else:
                return abort(422, description="Please enter a boolean value, true or false")
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
        try:
            return {
                "total_items": len(data),
                "data": data
            }
        except Exception as e:
            return jsonify({"An exception occurred": e})
    return app

# if __name__ == "__main__":
#     app.run(debug=True)

# Upload data DB
# f = open("src/data/users.json")
# data = json.load(f)
# for user in data:
#     users.insert_one(user)

# f = open("src/data/tasks.json")
# data = json.load(f)
# for task in data:
#     tasks.insert_one(task)