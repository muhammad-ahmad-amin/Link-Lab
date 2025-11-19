#ifndef RECOMMENDATION_ENGINE_H
#define RECOMMENDATION_ENGINE_H

#include "graph.h"
#include <memory>

class RecommendationEngine {
private:
    std::unique_ptr<RecommendationGraph> graph;
    
    // Weight factors for hybrid recommendation
    double collaborativeWeight;
    double contentBasedWeight;
    
public:
    RecommendationEngine();
    
    // Initialize with sample data
    void initializeSampleData();
    
    // Core recommendation methods
    std::vector<Movie> getRecommendations(const std::string& userId, 
                                         const std::string& method = "hybrid",
                                         int maxResults = 10);
    
    // User interaction methods
    void addUserRating(const std::string& userId, const std::string& movieId, int rating);
    void updateUserPreferences(const std::string& userId, 
                              const std::vector<std::string>& preferredGenres);
    
    // Analysis methods
    void analyzeUserBehavior(const std::string& userId);
    void generateSystemReport();
    
    // Configuration
    void setWeights(double collaborative, double contentBased);
    
    // Data persistence (simplified)
    void saveUserData(const std::string& filename);
    void loadUserData(const std::string& filename);
};

#endif