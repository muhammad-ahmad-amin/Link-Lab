from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# Import all data structures
from data_structures.graph import MusicGraph
from data_structures.heap import RecommendationHeap
from data_structures.trie import GenreTrie
from data_structures.bst import ArtistBST

# Import all algorithms
from algorithms.dijkstra import DijkstraAlgorithm
from algorithms.clustering import MusicClusterer
from algorithms.sorting import QuickSort, MergeSort

# Import utilities
from utils.analyzer import MusicAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize data structures (global instances)
music_graph = MusicGraph()
recommendation_heap = RecommendationHeap()
genre_trie = GenreTrie()
artist_bst = ArtistBST()
music_analyzer = MusicAnalyzer()

# Global storage
app_data = {
    'playlist': [],
    'recommendations': [],
    'users': [],
    'last_updated': None
}

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Main recommendation endpoint using ALL data structures and algorithms"""
    try:
        print("\n" + "="*60)
        print("🎵 Processing Recommendation Request...")
        print("="*60)
        
        data = request.json
        playlist = data.get('playlist', [])
        recommendations = data.get('recommendations', [])
        users = data.get('users', [])
        
        # Store data
        app_data['playlist'] = playlist
        app_data['recommendations'] = recommendations
        app_data['users'] = users
        app_data['last_updated'] = datetime.now().isoformat()
        
        print(f"📊 Received: {len(playlist)} playlist songs, {len(recommendations)} recommendations")
        
        # ==========================================
        # STEP 1: BUILD GRAPH STRUCTURE
        # ==========================================
        print("\n1️⃣  Building Graph (graph.py)...")
        music_graph.clear()
        
        for song in playlist + recommendations:
            music_graph.add_song(song)
        
        graph_result = music_graph.build_genre_graph(playlist, recommendations)
        print(f"   ✓ Graph built: {music_graph.node_count()} nodes, {music_graph.edge_count()} edges")
        print(f"   ✓ Graph density: {music_graph.get_graph_density():.2f}")
        
        # ==========================================
        # STEP 2: APPLY DIJKSTRA'S ALGORITHM
        # ==========================================
        print("\n2️⃣  Running Dijkstra's Algorithm (dijkstra.py)...")
        dijkstra = DijkstraAlgorithm(music_graph)
        distances = dijkstra.compute_shortest_paths()
        print(f"   ✓ Dijkstra completed in {dijkstra.execution_time:.4f}s")
        print(f"   ✓ Computed distances for {len(distances)} genres")
        
        # Find most central genre
        central_genre = dijkstra.find_most_central_genre()
        if central_genre:
            print(f"   ✓ Most central genre: {central_genre[0]}")
        
        # ==========================================
        # STEP 3: CALCULATE SCORES & USE MAX HEAP
        # ==========================================
        print("\n3️⃣  Using Max Heap for Priority (heap.py)...")
        recommendation_heap.clear()
        genre_scores = music_analyzer.calculate_genre_scores(playlist, recommendations, distances)
        
        for genre, score in genre_scores.items():
            recommendation_heap.insert(genre, score)
        
        print(f"   ✓ Heap built with {recommendation_heap.size()} items")
        print(f"   ✓ Heap property valid: {recommendation_heap.validate_heap_property()}")
        
        # Extract top recommendations
        top_recommendations = []
        heap_size = min(10, recommendation_heap.size())
        temp_heap = RecommendationHeap()
        temp_heap.heap = recommendation_heap.heap.copy()
        temp_heap.genre_map = recommendation_heap.genre_map.copy()
        
        for _ in range(heap_size):
            if temp_heap.size() > 0:
                top_recommendations.append(temp_heap.extract_max())
        
        print(f"   ✓ Top recommendation: {top_recommendations[0]['genre'] if top_recommendations else 'None'}")
        
        # ==========================================
        # STEP 4: BUILD TRIE FOR GENRE SEARCH
        # ==========================================
        print("\n4️⃣  Building Trie for Search (trie.py)...")
        genre_trie.clear()
        
        for genre in genre_scores.keys():
            genre_trie.insert(genre)
        
        trie_stats = genre_trie.get_statistics()
        print(f"   ✓ Trie indexed {trie_stats['total_words']} genres")
        print(f"   ✓ Max depth: {trie_stats['max_depth']}")
        
        # ==========================================
        # STEP 5: BUILD BST FOR ARTIST MANAGEMENT
        # ==========================================
        print("\n5️⃣  Building BST for Artists (bst.py)...")
        artist_bst.clear()
        artist_data = music_analyzer.analyze_artists(playlist, recommendations)
        
        for artist, count in artist_data.items():
            artist_bst.insert(artist, count)
        
        bst_stats = artist_bst.get_statistics()
        print(f"   ✓ BST built with {bst_stats['size']} artists")
        print(f"   ✓ Tree height: {bst_stats['height']}")
        print(f"   ✓ Tree balanced: {bst_stats['is_balanced']}")
        
        # ==========================================
        # STEP 6: APPLY CLUSTERING ALGORITHM
        # ==========================================
        print("\n6️⃣  Running K-Means Clustering (clustering.py)...")
        clusterer = MusicClusterer(k=5)
        clusters = clusterer.cluster_songs(playlist + recommendations)
        print(f"   ✓ Created {clusters['total_clusters']} clusters")
        print(f"   ✓ Clustering completed in {clusterer.execution_time:.4f}s")
        print(f"   ✓ Silhouette score: {clusters['silhouette_score']}")
        
        # ==========================================
        # STEP 7: SORT USING QUICKSORT & MERGESORT
        # ==========================================
        print("\n7️⃣  Sorting with Algorithms (sorting.py)...")
        quick_sorter = QuickSort()
        merge_sorter = MergeSort()
        
        ordered_genres_quick = quick_sorter.sort_by_score(genre_scores)
        ordered_genres_merge = merge_sorter.sort_by_distance(distances)
        
        print(f"   ✓ QuickSort: {quick_sorter.comparison_count} comparisons in {quick_sorter.execution_time:.6f}s")
        print(f"   ✓ MergeSort: {merge_sorter.comparison_count} comparisons in {merge_sorter.execution_time:.6f}s")
        
        # ==========================================
        # STEP 8: FLATTEN EDGES FOR FRONTEND
        # ==========================================
        raw_graph = graph_result['edges'] if 'edges' in graph_result else []
        flat_edges = []
        seen_pairs = set()
        
        # If edges not in expected format, build from adjacency list
        if not raw_graph:
            adjacency_list = music_graph.get_adjacency_list()
            for source, targets in adjacency_list.items():
                for target_data in targets:
                    target = target_data['to']
                    pair = tuple(sorted((source, target)))
                    if pair not in seen_pairs:
                        flat_edges.append({
                            'from': source,
                            'to': target,
                            'weight': target_data['weight']
                        })
                        seen_pairs.add(pair)
        else:
            flat_edges = raw_graph
        
        # ==========================================
        # PREPARE FINAL RESPONSE
        # ==========================================
        print("\n✅ All data structures processed successfully!")
        print("="*60 + "\n")
        
        response_data = {
            'success': True,
            'orderedGenres': ordered_genres_quick,
            'genreCounts': graph_result['genre_counts'],
            'artistCounts': dict(list(artist_data.items())[:10]),
            'recommendationScores': genre_scores,
            'topRecommendations': top_recommendations,
            'distances': distances,
            'clusters': {
                'total': clusters['total_clusters'],
                'sizes': clusters['cluster_sizes'],
                'silhouette_score': clusters['silhouette_score']
            },
            'graphStructure': {
                'nodes': list(graph_result['genre_counts'].keys()),
                'edges': flat_edges,
                'adjacency_list': music_graph.get_adjacency_list(),
                'density': music_graph.get_graph_density()
            },
            'trieStats': trie_stats,
            'bstStats': {
                'total_artists': bst_stats['size'],
                'height': bst_stats['height'],
                'is_balanced': bst_stats['is_balanced'],
                'inorder': artist_bst.inorder_traversal()[:10],
                'min_artist': bst_stats['min'],
                'max_artist': bst_stats['max']
            },
            'algorithmMetrics': {
                'dijkstra_time': dijkstra.execution_time,
                'clustering_time': clusterer.execution_time,
                'quicksort_comparisons': quick_sorter.comparison_count,
                'quicksort_time': quick_sorter.execution_time,
                'mergesort_comparisons': merge_sorter.comparison_count,
                'mergesort_time': merge_sorter.execution_time,
                'graph_nodes': music_graph.node_count(),
                'graph_edges': music_graph.edge_count(),
                'heap_size': recommendation_heap.size()
            },
            'insights': music_analyzer.generate_insights(playlist, recommendations),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"\n❌ Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-genre', methods=['POST'])
def search_genre():
    """Search genres using Trie"""
    try:
        data = request.json
        prefix = data.get('prefix', '')
        
        matches = genre_trie.search_prefix(prefix)
        
        print(f"🔍 Genre search for '{prefix}': {len(matches)} matches")
        
        return jsonify({
            'success': True,
            'matches': matches,
            'count': len(matches)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/artist-range', methods=['POST'])
def get_artist_range():
    """Get artists in a range using BST"""
    try:
        data = request.json
        min_count = data.get('min_count', 0)
        max_count = data.get('max_count', float('inf'))
        
        artists = artist_bst.range_query(min_count, max_count)
        
        print(f"🎤 Artist range query [{min_count}, {max_count}]: {len(artists)} results")
        
        return jsonify({
            'success': True,
            'artists': artists
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/graph-data', methods=['GET'])
def get_graph_data():
    """Get detailed graph structure"""
    try:
        adjacency_list = music_graph.get_adjacency_list()
        
        nodes = []
        links = []
        
        for node, edges in adjacency_list.items():
            nodes.append({
                'id': node,
                'label': node,
                'degree': len(edges)
            })
            
            for edge in edges:
                links.append({
                    'source': node,
                    'target': edge['to'],
                    'weight': edge['weight']
                })
        
        return jsonify({
            'success': True,
            'nodes': nodes,
            'links': links,
            'total_nodes': len(nodes),
            'total_edges': len(links),
            'density': music_graph.get_graph_density()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics"""
    try:
        stats = {
            'playlist_size': len(app_data.get('playlist', [])),
            'recommendations_size': len(app_data.get('recommendations', [])),
            'graph_stats': {
                'nodes': music_graph.node_count(),
                'edges': music_graph.edge_count(),
                'density': music_graph.get_graph_density()
            },
            'heap_size': recommendation_heap.size(),
            'trie_words': genre_trie.count_words(),
            'bst_size': artist_bst.size(),
            'bst_height': artist_bst.height(),
            'last_updated': app_data.get('last_updated')
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_structures': {
            'graph': 'initialized',
            'heap': 'initialized',
            'trie': 'initialized',
            'bst': 'initialized'
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🎵 MUSIC RECOMMENDATION SYSTEM - DSA PROJECT")
    print("=" * 70)
    print("\n📊 Data Structures Implemented:")
    print("   ✓ Graph (Adjacency List) - graph.py")
    print("   ✓ Max Heap (Priority Queue) - heap.py")
    print("   ✓ Trie (Genre Search) - trie.py")
    print("   ✓ Binary Search Tree (Artist Management) - bst.py")
    print("\n🔧 Algorithms Implemented:")
    print("   ✓ Dijkstra's Shortest Path - dijkstra.py")
    print("   ✓ QuickSort - sorting.py")
    print("   ✓ MergeSort - sorting.py")
    print("   ✓ K-Means Clustering - clustering.py")
    print("\n🌐 Server running on http://localhost:5000")
    print("📡 API Endpoints:")
    print("   - POST /api/recommend")
    print("   - POST /api/search-genre")
    print("   - POST /api/artist-range")
    print("   - GET  /api/graph-data")
    print("   - GET  /api/stats")
    print("   - GET  /health")
    print("\n" + "=" * 70)
    print("Ready to process recommendations! 🚀")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)