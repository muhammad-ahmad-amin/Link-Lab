#ifndef GRAPH_H
#define GRAPH_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <queue>
#include <algorithm>
#include <cmath>

// User node in the graph
struct User {
    std::string id;
    std::string name;
    std::vector<std::string> preferredGenres;
    std::unordered_map<std::string, int> ratings; // movieId -> rating
    
    User(const std::string& uid, const std::string& uname) 
        : id(uid), name(uname) {}
};

// Movie node in the graph
struct Movie {
    std::string id;
    std::string title;
    std::string genre;
    double rating;
    int year;
    
    Movie(const std::string& mid, const std::string& mtitle, 
          const std::string& mgenre, double mrating, int myear)
        : id(mid), title(mtitle), genre(mgenre), rating(mrating), year(myear) {}
};

// Genre node in the graph
struct Genre {
    std::string id;
    std::string name;
    
    Genre(const std::string& gid, const std::string& gname)
        : id(gid), name(gname) {}
};

// Edge between nodes
struct Edge {
    std::string from;
    std::string to;
    int weight;
    std::string type; // "rated", "prefers", "belongs_to"
    
    Edge(const std::string& f, const std::string& t, int w, const std::string& typ)
        : from(f), to(t), weight(w), type(typ) {}
};

// Graph class for the recommendation system
class RecommendationGraph {
private:
    std::unordered_map<std::string, User> users;
    std::unordered_map<std::string, Movie> movies;
    std::unordered_map<std::string, Genre> genres;
    std::unordered_map<std::string, std::vector<Edge>> adjacencyList;
    
    // Similarity calculation between users
    double calculateUserSimilarity(const User& user1, const User& user2);
    
    // Find common movies between users
    std::vector<std::string> getCommonMovies(const User& user1, const User& user2);
    
    // BFS traversal for finding connections
    std::vector<std::string> BFS(const std::string& startNode, int maxDepth);

public:
    RecommendationGraph();
    
    // Node management
    void addUser(const std::string& id, const std::string& name, 
                 const std::vector<std::string>& preferredGenres);
    void addMovie(const std::string& id, const std::string& title, 
                  const std::string& genre, double rating, int year);
    void addGenre(const std::string& id, const std::string& name);
    
    // Edge management
    void addRating(const std::string& userId, const std::string& movieId, int rating);
    void addGenrePreference(const std::string& userId, const std::string& genreId);
    
    // Recommendation algorithms
    std::vector<Movie> getCollaborativeFilteringRecommendations(const std::string& userId, 
                                                               int maxRecommendations = 10);
    std::vector<Movie> getContentBasedRecommendations(const std::string& userId, 
                                                     int maxRecommendations = 10);
    std::vector<Movie> getHybridRecommendations(const std::string& userId, 
                                               int maxRecommendations = 10);
    
    // Graph analysis
    std::vector<std::string> findSimilarUsers(const std::string& userId, 
                                             double similarityThreshold = 0.5);
    std::vector<std::string> getMovieRecommendationPath(const std::string& userId, 
                                                       const std::string& movieId);
    
    // Utility functions
    void printGraphStats();
    std::vector<std::string> getTopRatedMovies(int count = 5);
    std::vector<std::string> getPopularMoviesByGenre(const std::string& genre, int count = 5);
    
    // Getters
    const User& getUser(const std::string& userId) const { return users.at(userId); }
    const Movie& getMovie(const std::string& movieId) const { return movies.at(movieId); }
    const std::unordered_map<std::string, User>& getAllUsers() const { return users; }
    const std::unordered_map<std::string, Movie>& getAllMovies() const { return movies; }
};

#endif