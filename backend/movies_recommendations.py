from flask import Flask, request, jsonify
from collections import defaultdict
import math

app = Flask(__name__)


def analyze_genres(payload):
    watchlist = payload.get("watchlist", [])
    users = payload.get("users", [])

    # Count genre frequency
    genre_count = defaultdict(int)

    for movie in watchlist:
        genres = movie.get("genres", [])
        for g in genres:
            genre_count[g] += 1

    for user in users:
        pref = user.get("preferences", {}).get("movies")
        if pref:
            genre_count[pref] += 1

    # If no genres found then return defaults
    if not genre_count:
        return ["Action", "Drama", "Comedy", "Thriller", "Sci-Fi"]

    genres_list = list(genre_count.keys())

    # Build weighted graph (fully connected)
    graph = {g: [] for g in genres_list}
    for i in range(len(genres_list)):
        for j in range(i+1, len(genres_list)):
            g1, g2 = genres_list[i], genres_list[j]
            w = 1 + abs(genre_count[g1] - genre_count[g2])
            graph[g1].append((g2, w))
            graph[g2].append((g1, w))

    # Dijkstra-style distances using a stack
    dist = {g: float('inf') for g in genres_list}
    source = genres_list[0]
    dist[source] = 0

    stack = [source]
    while stack:
        current = stack.pop()
        for to, weight in graph[current]:
            if dist[current] + weight < dist[to]:
                dist[to] = dist[current] + weight
                stack.append(to)

    # Sort by distance
    sorted_list = sorted(dist.items(), key=lambda x: x[1])

    return [genre for genre, score in sorted_list]


@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        payload = request.get_json()
    except:
        return "Invalid JSON", 400

    ordered = analyze_genres(payload)
    return jsonify(ordered)


if __name__ == "__main__":
    print("Server running on port 8080...")
    app.run(host="0.0.0.0", port=8080)