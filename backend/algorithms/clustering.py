"""
K-Means Clustering Algorithm
Groups similar songs together based on their attributes
"""

import time
import random
from collections import defaultdict

class MusicClusterer:
    def __init__(self, k=5):
        self.k = k  # Number of clusters
        self.execution_time = 0
        self.centroids = []
        self.labels = []
        
    def cluster_songs(self, songs, max_iterations=100):
        """
        Cluster songs using K-Means algorithm
        Songs are represented by genre and artist features
        """
        start_time = time.time()
        
        if len(songs) == 0:
            self.execution_time = time.time() - start_time
            return {}
        
        # Adjust k if we have fewer songs
        k = min(self.k, len(songs))
        
        # Extract features from songs
        features = self._extract_features(songs)
        
        # Initialize centroids randomly
        self.centroids = random.sample(features, k)
        
        # K-Means iterations
        for iteration in range(max_iterations):
            # Assign each point to nearest centroid
            clusters = self._assign_to_clusters(features, self.centroids)
            
            # Calculate new centroids
            new_centroids = self._calculate_centroids(clusters)
            
            # Check for convergence
            if self._has_converged(self.centroids, new_centroids):
                break
            
            self.centroids = new_centroids
        
        # Assign labels
        self.labels = [self._find_nearest_centroid(f, self.centroids) for f in features]
        
        self.execution_time = time.time() - start_time
        
        # Prepare result
        result = self._prepare_result(songs, self.labels)
        
        return result
    
    def _extract_features(self, songs):
        """
        Extract numerical features from songs
        Feature vector: [genre_id, artist_hash, price]
        """
        # Create mappings for genres and artists
        genres = list(set(song.get('genre', 'Unknown') for song in songs))
        artists = list(set(song.get('artist', 'Unknown') for song in songs))
        
        genre_to_id = {genre: i for i, genre in enumerate(genres)}
        artist_to_id = {artist: i for i, artist in enumerate(artists)}
        
        features = []
        for song in songs:
            genre = song.get('genre', 'Unknown')
            artist = song.get('artist', 'Unknown')
            price = song.get('price', 0) or 0
            
            feature = [
                genre_to_id.get(genre, 0),
                artist_to_id.get(artist, 0),
                float(price) * 10  # Scale price
            ]
            features.append(feature)
        
        return features
    
    def _euclidean_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5
    
    def _find_nearest_centroid(self, point, centroids):
        """Find the index of the nearest centroid"""
        distances = [self._euclidean_distance(point, centroid) for centroid in centroids]
        return distances.index(min(distances))
    
    def _assign_to_clusters(self, features, centroids):
        """Assign each feature vector to the nearest centroid"""
        clusters = defaultdict(list)
        
        for feature in features:
            cluster_id = self._find_nearest_centroid(feature, centroids)
            clusters[cluster_id].append(feature)
        
        return clusters
    
    def _calculate_centroids(self, clusters):
        """Calculate new centroids as mean of cluster points"""
        new_centroids = []
        
        for cluster_id in range(self.k):
            if cluster_id in clusters and clusters[cluster_id]:
                points = clusters[cluster_id]
                n_features = len(points[0])
                
                # Calculate mean for each dimension
                centroid = [
                    sum(point[i] for point in points) / len(points)
                    for i in range(n_features)
                ]
                new_centroids.append(centroid)
            else:
                # If cluster is empty, keep old centroid or create random
                if cluster_id < len(self.centroids):
                    new_centroids.append(self.centroids[cluster_id])
                else:
                    new_centroids.append([0] * len(self.centroids[0]))
        
        return new_centroids
    
    def _has_converged(self, old_centroids, new_centroids, threshold=0.001):
        """Check if centroids have converged"""
        if len(old_centroids) != len(new_centroids):
            return False
        
        for old, new in zip(old_centroids, new_centroids):
            if self._euclidean_distance(old, new) > threshold:
                return False
        
        return True
    
    def _prepare_result(self, songs, labels):
        """Prepare clustering result"""
        clusters = defaultdict(list)
        
        for i, song in enumerate(songs):
            cluster_id = labels[i]
            clusters[f'cluster_{cluster_id}'].append({
                'title': song.get('title', 'Unknown'),
                'artist': song.get('artist', 'Unknown'),
                'genre': song.get('genre', 'Unknown')
            })
        
        # Calculate cluster statistics
        result = {
            'clusters': dict(clusters),
            'cluster_sizes': {k: len(v) for k, v in clusters.items()},
            'total_clusters': len(clusters),
            'silhouette_score': self._calculate_silhouette_score(labels)
        }
        
        return result
    
    def _calculate_silhouette_score(self, labels):
        """
        Calculate simplified silhouette score
        Measures how well clustered the data is
        """
        if len(set(labels)) <= 1:
            return 0.0
        
        # Simplified calculation
        cluster_counts = defaultdict(int)
        for label in labels:
            cluster_counts[label] += 1
        
        # Higher score if clusters are more balanced
        ideal_size = len(labels) / len(set(labels))
        variance = sum((count - ideal_size) ** 2 for count in cluster_counts.values())
        
        # Normalize to [0, 1]
        score = 1.0 / (1.0 + variance / len(labels))
        
        return round(score, 3)
    
    def predict_cluster(self, song_features):
        """Predict which cluster a new song belongs to"""
        if not self.centroids:
            return -1
        
        return self._find_nearest_centroid(song_features, self.centroids)
    
    def get_cluster_summary(self):
        """Get summary statistics for each cluster"""
        if not self.labels:
            return {}
        
        summary = defaultdict(lambda: {'count': 0, 'density': 0})
        
        for label in self.labels:
            summary[label]['count'] += 1
        
        return dict(summary)
    
    def elbow_method(self, songs, max_k=10):
        """
        Use elbow method to find optimal number of clusters
        Returns list of (k, inertia) tuples
        """
        features = self._extract_features(songs)
        results = []
        
        for k in range(2, min(max_k + 1, len(songs))):
            self.k = k
            self.cluster_songs(songs, max_iterations=50)
            
            # Calculate inertia (within-cluster sum of squares)
            inertia = self._calculate_inertia(features)
            results.append((k, inertia))
        
        return results
    
    def _calculate_inertia(self, features):
        """Calculate within-cluster sum of squared distances"""
        inertia = 0
        
        for i, feature in enumerate(features):
            cluster_id = self.labels[i]
            centroid = self.centroids[cluster_id]
            inertia += self._euclidean_distance(feature, centroid) ** 2
        
        return inertia