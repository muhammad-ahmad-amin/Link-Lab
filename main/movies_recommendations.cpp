// Libraries
#include "crow.h"
#include <vector>
#include <string>
#include <map>
#include <queue>
#include <stack>
#include <set>
#include <algorithm>
#include <limits>

// Genre
struct GenreScore {
    std::string genre;
    int score;
};

// Edge
struct Edge {
    std::string to;
    int weight;
};

// Main code
std::vector<std::string> analyzeGenres(const crow::json::rvalue& payload) {
    auto watchlist = payload["watchlist"];
    auto users = payload["users"];

    std::map<std::string, int> genreCount;

    // Count frequencies
    for (auto& movie : watchlist) {
        if (movie.has("genres")) {
            for (auto& g : movie["genres"]) {
                genreCount[g.s()]++;
            }
        }
    }
    for (auto& user : users) {
        if (user.has("preferences") && user["preferences"].has("movies")) {
            std::string moviePref = user["preferences"]["movies"].s();
            genreCount[moviePref]++;
        }
    }

    if (genreCount.empty())
        return {"Action", "Drama", "Comedy", "Thriller", "Sci-Fi"};

    // Build a graph where genres are nodes, edges connect co-occurring genres
    std::map<std::string, std::vector<Edge>> graph;
    std::vector<std::string> genresList;
    for (auto& [genre, count] : genreCount) {
        genresList.push_back(genre);
    }

    // Fully connect all genres with weight inversely proportional to frequency
    for (size_t i = 0; i < genresList.size(); ++i) {
        for (size_t j = i + 1; j < genresList.size(); ++j) {
            int w = 1 + std::abs(genreCount[genresList[i]] - genreCount[genresList[j]]);
            graph[genresList[i]].push_back({genresList[j], w});
            graph[genresList[j]].push_back({genresList[i], w});
        }
    }

    // Dijkstra to compute distances from a dummy source
    std::map<std::string, int> dist;
    for (auto& [g, _] : genreCount) dist[g] = std::numeric_limits<int>::max();

    // Use a stack to simulate priority queue processing (just for DSA flavor)
    std::stack<std::string> stackNodes;
    auto source = genresList[0];
    dist[source] = 0;
    stackNodes.push(source);

    while (!stackNodes.empty()) {
        std::string current = stackNodes.top();
        stackNodes.pop();

        for (auto& edge : graph[current]) {
            if (dist[current] + edge.weight < dist[edge.to]) {
                dist[edge.to] = dist[current] + edge.weight;
                stackNodes.push(edge.to); // push updated node
            }
        }
    }

    // Sort genres by computed distance
    std::vector<GenreScore> sortedGenres;
    for (auto& [genre, d] : dist) {
        sortedGenres.push_back({genre, d});
    }

    std::sort(sortedGenres.begin(), sortedGenres.end(),
              [](const GenreScore& a, const GenreScore& b) { return a.score < b.score; });

    std::vector<std::string> orderedGenres;
    for (auto& g : sortedGenres) orderedGenres.push_back(g.genre);

    return orderedGenres;
}

int main() {
    crow::SimpleApp app;

    CROW_CATCHALL_ROUTE(app)([](const crow::request& req, crow::response& res){
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        res.add_header("Access-Control-Allow-Headers", "Content-Type, Authorization");
        if (req.method == "OPTIONS"_method) res.end();
    });

    CROW_ROUTE(app, "/recommend").methods("POST"_method)([](const crow::request& req){
        auto payload = crow::json::load(req.body);
        if(!payload) return crow::response(400, "Invalid JSON");

        auto orderedGenres = analyzeGenres(payload);

        crow::json::wvalue result;
        int idx = 0;
        for (auto& g : orderedGenres) {
            result[idx] = g;
            idx++;
        }

        return crow::response(result);
    });

    std::cout << "Server running on port 8080..." << std::endl;
    app.port(8080).multithreaded().run();
}