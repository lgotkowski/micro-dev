from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)


tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "milk, cheese, pizza",
        "done": False
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Need to fin tutorial.",
        "done": False
    }
]


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    public_tasks = [make_public_task(task) for task in tasks]
    return jsonify({"tasks": public_tasks})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    task_match = [task for task in tasks if task["id"] == task_id]
    if not task_match:
        abort(404)
    public_tasks = [make_public_task(task) for task in task_match]
    return jsonify({"task": public_tasks[0]})


@app.route("/todo/api/v1.0/tasks", methods=["POST"])
@auth.login_required
def create_task():
    if not request.json or not "title" in request.json:
        abort(400)

    task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "done": False
    }
    tasks.append(task)
    public_task = make_public_task(task)
    return jsonify({"task": public_task}), 201


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if not task:
        abort(404)
    if not request.json:
        abort(404)
    if "title" in request.json and type(request.json["title"]) != unicode:
        abort(404)
    if "description" in request.json and type(request.json["description"]) != unicode:
        abort(404)
    if "done" in request.json and type(request.json["dont"]) != bool:
        abort(404)

    task[0]["title"] = request.json.get("title", task[0]["title"])
    task[0]["description"] = request.json.get("description", task[0]["description"])
    task[0]["done"] = request.json.get("done", task[0]["done"])

    public_task = make_public_task(task[0])
    return jsonify({"task": public_task})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["DELETE"])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if not task:
        abort(404)

    tasks.remove(task[0])
    return jsonify({"result": True})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == "id":
            new_task["uri"] = url_for("get_task", task_id=task["id"], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@auth.get_password
def get_password(username):
    if username == "lukas":
        return "1234"
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World!"})


if __name__ == "__main__":
    with app.test_request_context():
        print(url_for("index"))
        print(url_for("get_task", task_id=1))
    app.run(debug=True)

