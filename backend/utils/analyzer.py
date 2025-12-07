"""
Music Analyzer Utility
Provides analysis functions for music data
"""

from collections import Counter, defaultdict

class MusicAnalyzer:
    def __init__(self):
        pass
    
    def calculate_genre_scores(self, playlist, recommendations, distances):
        """
        Calculate recommendation scores for each genre
        Score = frequency / (1 + distance)
        """
        # Count genres
        genre_counts = Counter()
        
        for song in playlist:
            if song.get('genre'):
                genre_counts[song['genre']] += 1
        
        for song in recommendations:
            if song.get('genre'):
                genre_counts[song['genre']] += 2  # Weight recommendations higher
        
        # Calculate scores using distances
        scores = {}
        for genre, count in genre_counts.items():
            distance = distances.get(genre, float('inf'))
            if distance == float('inf'):
                scores[genre] = count
            else:
                scores[genre] = round(count / (1 + distance), 2)
        
        return scores
    
    def analyze_artists(self, playlist, recommendations):
        """Analyze artist frequencies"""
        artist_counts = Counter()
        
        for song in playlist:
            if song.get('artist'):
                artist_counts[song['artist']] += 1
        
        for song in recommendations:
            if song.get('artist'):
                artist_counts[song['artist']] += 2
        
        return dict(artist_counts)
    
    def analyze_temporal_patterns(self, playlist):
        """Analyze when songs were added"""
        patterns = {
            'total_songs': len(playlist),
            'genres_distribution': self._genre_distribution(playlist),
            'artist_diversity': self._calculate_diversity(playlist, 'artist'),
            'genre_diversity': self._calculate_diversity(playlist, 'genre')
        }
        
        return patterns
    
    def _genre_distribution(self, songs):
        """Calculate genre distribution"""
        genres = [song.get('genre', 'Unknown') for song in songs]
        counter = Counter(genres)
        
        return {
            'counts': dict(counter),
            'percentages': {
                genre: round(count / len(songs) * 100, 2)
                for genre, count in counter.items()
            }
        }
    
    def _calculate_diversity(self, songs, field):
        """
        Calculate Shannon diversity index
        Higher value means more diverse
        """
        values = [song.get(field, 'Unknown') for song in songs]
        counter = Counter(values)
        
        total = len(values)
        if total == 0:
            return 0
        
        # Shannon entropy
        diversity = 0
        for count in counter.values():
            proportion = count / total
            if proportion > 0:
                diversity -= proportion * (proportion ** 0.5)  # Simplified
        
        return round(diversity, 3)
    
    def find_similar_songs(self, target_song, all_songs, top_k=5):
        """
        Find songs similar to target song
        Based on genre and artist matching
        """
        target_genre = target_song.get('genre', '')
        target_artist = target_song.get('artist', '')
        
        similarities = []
        
        for song in all_songs:
            if song.get('id') == target_song.get('id'):
                continue
            
            score = 0
            
            # Genre match (weight: 3)
            if song.get('genre') == target_genre:
                score += 3
            
            # Artist match (weight: 2)
            if song.get('artist') == target_artist:
                score += 2
            
            # Same album (weight: 1)
            if song.get('album') == target_song.get('album'):
                score += 1
            
            if score > 0:
                similarities.append({
                    'song': song,
                    'similarity_score': score
                })
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities[:top_k]
    
    def calculate_listening_score(self, playlist):
        """
        Calculate overall listening score based on diversity and variety
        """
        if not playlist:
            return 0
        
        scores = {
            'diversity': self._calculate_diversity(playlist, 'genre') * 20,
            'artist_variety': self._calculate_diversity(playlist, 'artist') * 15,
            'size_bonus': min(len(playlist) / 10, 10),  # Max 10 points
        }
        
        total_score = sum(scores.values())
        
        return {
            'total_score': round(total_score, 2),
            'breakdown': scores,
            'rating': self._get_rating(total_score)
        }
    
    def _get_rating(self, score):
        """Convert score to rating"""
        if score >= 40:
            return 'Excellent'
        elif score >= 30:
            return 'Great'
        elif score >= 20:
            return 'Good'
        elif score >= 10:
            return 'Fair'
        else:
            return 'Limited'
    
    def generate_insights(self, playlist, recommendations):
        """Generate insights about music preferences"""
        insights = []
        
        # Genre insights
        genre_counts = Counter(song.get('genre', 'Unknown') for song in playlist)
        if genre_counts:
            top_genre = genre_counts.most_common(1)[0]
            insights.append({
                'type': 'genre_preference',
                'message': f"You love {top_genre[0]}! It makes up {round(top_genre[1]/len(playlist)*100)}% of your playlist."
            })
        
        # Artist insights
        artist_counts = Counter(song.get('artist', 'Unknown') for song in playlist)
        if len(artist_counts) > 5:
            insights.append({
                'type': 'artist_diversity',
                'message': f"Great variety! You listen to {len(artist_counts)} different artists."
            })
        
        # Recommendations insights
        if recommendations:
            rec_genres = Counter(song.get('genre', 'Unknown') for song in recommendations)
            if rec_genres:
                top_rec = rec_genres.most_common(1)[0]
                insights.append({
                    'type': 'recommendation_focus',
                    'message': f"Your recommendations show interest in {top_rec[0]}."
                })
        
        return insights
    
    def compare_playlists(self, playlist1, playlist2):
        """Compare two playlists"""
        genres1 = set(song.get('genre') for song in playlist1 if song.get('genre'))
        genres2 = set(song.get('genre') for song in playlist2 if song.get('genre'))
        
        common_genres = genres1.intersection(genres2)
        unique1 = genres1 - genres2
        unique2 = genres2 - genres1
        
        return {
            'common_genres': list(common_genres),
            'unique_to_first': list(unique1),
            'unique_to_second': list(unique2),
            'similarity_score': round(len(common_genres) / len(genres1.union(genres2)) * 100, 2) if genres1.union(genres2) else 0
        }
    
    def predict_next_preference(self, playlist, recommendations):
        """Predict what genre user might like next"""
        # Combine all data
        all_genres = []
        
        for song in playlist:
            if song.get('genre'):
                all_genres.append(song['genre'])
        
        for song in recommendations:
            if song.get('genre'):
                all_genres.extend([song['genre']] * 2)  # Weight recommendations
        
        if not all_genres:
            return None
        
        # Find most common
        genre_counts = Counter(all_genres)
        
        # Get top 3
        top_genres = genre_counts.most_common(3)
        
        return {
            'primary_prediction': top_genres[0][0] if top_genres else None,
            'confidence': round(top_genres[0][1] / len(all_genres) * 100, 2) if top_genres else 0,
            'alternatives': [g[0] for g in top_genres[1:]]
        }