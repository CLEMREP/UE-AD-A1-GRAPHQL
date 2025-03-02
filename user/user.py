from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/users/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    res = requests.get("http://localhost:3201/bookings/{}".format(userid)).json()
    return make_response(res)

@app.route("/users/infomovies/<userid>", methods=['GET'])
def get_user_movies(userid):
    res = requests.get("http://localhost:3201/bookings/{}".format(userid)).json()
    movies = []
    rvalue = []
    if 'dates' not in res:
        return make_response(jsonify({"error":"No books found for this UserID"}),400)

    for movie in res['dates'][0]['movies']:
        print(movie)
        query = """
        query {
            movie_with_id(_id: """ + '''"''' + str(movie) + '''"''' + """) {id title}
        }
        """
        print(requests.post("http://localhost:3001/graphql", json={'query': query}).json())
        movies.append(requests.post("http://localhost:3001/graphql", json={'query': query}).json()['data']['movie_with_id'])
        print(movies)

    for movie in movies:
        query = """
        query {
            movie_with_id(_id: """ + '''"''' + str(movie['id']) + '''"''' + """) {id title}
        }
        """
        rvalue.append(requests.post("http://localhost:3001/graphql", json={'query': query}).json())

    return make_response(jsonify(rvalue), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
