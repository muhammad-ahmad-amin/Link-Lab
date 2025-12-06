from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store recommendation data in memory
recommendation_data = {
    'genre_counts': {},
    'artist_counts': {},
    'recommendation_scores': {},
    'graph_data': {}
}

def calculate_genre_graph(playlist, recommendations):
    """Build a weighted graph based on genre frequencies"""
    genre_count = Counter()
    
    # Count genres from playlist
    for song in playlist:
        if song.get('genre'):
            genre_count[song['genre']] += 1
    
    # Count genres from recommendations (with higher weight)
    for song in recommendations:
        if song.get('genre'):
            genre_count[song['genre']] += 2
    
    # Fallback if no data
    if not genre_count:
        genre_count = Counter({'Pop': 5, 'Rock': 3, 'Hip Hop': 2, 'Jazz': 1})
    
    # Build graph structure
    genres = list(genre_count.keys())
    graph = {genre: [] for genre in genres}
    
    # Create weighted edges between all genre pairs
    for i, g1 in enumerate(genres):
        for g2 in genres[i+1:]:
            # Weight calculation: closer counts = stronger connection
            weight = 1 + abs(genre_count[g1] - genre_count[g2])
            graph[g1].append({'to': g2, 'weight': weight})
            graph[g2].append({'to': g1, 'weight': weight})
    
    # Run Dijkstra-like algorithm for priority
    distances = {genre: float('inf') for genre in genres}
    if genres:
        source = genres[0] # Assume most popular is source
        distances[source] = 0
        
        stack = [source]
        while stack:
            current = stack.pop()
            for edge in graph.get(current, []):
                new_dist = distances[current] + edge['weight']
                if new_dist < distances[edge['to']]:
                    distances[edge['to']] = new_dist
                    stack.append(edge['to'])
    
    # Sort genres by distance (lower = higher priority)
    ordered_genres = sorted(distances.items(), key=lambda x: x[1])
    
    return {
        'genre_counts': dict(genre_count),
        'ordered_genres': [g[0] for g in ordered_genres],
        'distances': dict(distances),
        'graph': graph
    }

def calculate_artist_popularity(playlist, recommendations):
    """Calculate artist popularity scores"""
    artist_count = Counter()
    
    for song in playlist:
        if song.get('artist'):
            artist_count[song['artist']] += 1
    
    for song in recommendations:
        if song.get('artist'):
            artist_count[song['artist']] += 2

    # Fallback mock data if empty
    if not artist_count:
        artist_count = Counter({'The Weeknd': 10, 'Drake': 8, 'Taylor Swift': 5})
    
    return dict(artist_count.most_common(10))

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Main recommendation endpoint"""
    try:
        data = request.json
        playlist = data.get('playlist', [])
        recommendations = data.get('recommendations', [])
        
        # 1. Calculate Backend Logic
        graph_data = calculate_genre_graph(playlist, recommendations)
        artist_data = calculate_artist_popularity(playlist, recommendations)
        
        # 2. Store data globally (optional)
        recommendation_data['genre_counts'] = graph_data['genre_counts']
        
        # 3. Calculate Scores
        scores = {}
        for genre, count in graph_data['genre_counts'].items():
            distance = graph_data['distances'].get(genre, 1)
            # Avoid division by zero
            scores[genre] = round(count / (1 + distance), 2)
        
        # 4. CRITICAL FIX: Flatten edges for Frontend
        # The frontend expects an array of objects: [{from: 'A', to: 'B', weight: 1}, ...]
        raw_graph = graph_data['graph']
        flat_edges = []
        seen_pairs = set()

        for source, targets in raw_graph.items():
            for target_data in targets:
                target = target_data['to']
                # Create a unique key for the pair to avoid duplicate lines in visualization
                pair = tuple(sorted((source, target)))
                if pair not in seen_pairs:
                    flat_edges.append({
                        'from': source,
                        'to': target,
                        'weight': target_data['weight']
                    })
                    seen_pairs.add(pair)

        # 5. Send Response
        return jsonify({
            'success': True,
            'orderedGenres': graph_data['ordered_genres'],
            'genreCounts': graph_data['genre_counts'],
            'artistCounts': artist_data,
            'recommendationScores': scores,
            'distances': graph_data['distances'],
            'graphStructure': {
                'nodes': list(graph_data['genre_counts'].keys()),
                'edges': flat_edges  # <--- Sending the flattened array here
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error processing request: {e}") # Print error to Python console
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🎵 Music Recommendation Server Starting...")
    print("📊 Server running on http://localhost:5000")
    # debug=True allows you to see errors in the terminal
    app.run(debug=True, port=5000)