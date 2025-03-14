from flask import (
    Flask,
    request as flask_request,
    render_template
)
import requests
from flask import redirect, url_for

app = Flask(__name__)
BACKEND_URL="http://127.0.0.1:5000/tasks"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/tasks")
def get_task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list) 
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/")
def get_single_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("detail.html", task=single_task)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

# Update
@app.get("/tasks/<int:pk>/edit/")
def get_edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("edit.html", task=single_task)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit/")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    task_data = flask_request.form      # the form attribute will give us a dictionary
    response = requests.put(url, json=task_data)    # note the PUT request
    if response.status_code == 204:
        return render_template("success.html", message="Task edited")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

# Create
@app.get("/tasks/create/")
def get_create_form():
    return render_template("create.html")

@app.post("/tasks/create/")
def create_task():
    task_data = flask_request.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 201:
        return render_template("success.html", message="Task created successfully")
    return (
        render_template("error.html", error=response.status_code), 
        response.status_code
    )

# Delete
@app.get("/tasks/<int:pk>/delete/")
def delete_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 200:
        return redirect(url_for("get_task_list"))
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )