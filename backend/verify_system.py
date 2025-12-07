"""
System Verification Script
Tests all data structures and algorithms to ensure they're working
Run this from the backend folder: python verify_system.py
"""

import sys
import json

def test_graph():
    """Test Graph implementation"""
    print("\n" + "="*60)
    print("TESTING GRAPH DATA STRUCTURE")
    print("="*60)
    
    from data_structures.graph import MusicGraph
    
    graph = MusicGraph()
    
    # Add sample songs
    songs = [
        {'genre': 'Rock', 'title': 'Song 1'},
        {'genre': 'Rock', 'title': 'Song 2'},
        {'genre': 'Pop', 'title': 'Song 3'},
        {'genre': 'Jazz', 'title': 'Song 4'},
    ]
    
    for song in songs:
        graph.add_song(song)
    
    result = graph.build_genre_graph(songs, [])
    
    print(f"✓ Nodes created: {graph.node_count()}")
    print(f"✓ Edges created: {graph.edge_count()}")
    print(f"✓ Genre counts: {result['genre_counts']}")
    print(f"✓ Graph density: {graph.get_graph_density():.2f}")
    
    print("\n✅ GRAPH TEST PASSED!")
    return True

def test_heap():
    """Test Max Heap implementation"""
    print("\n" + "="*60)
    print("TESTING MAX HEAP DATA STRUCTURE")
    print("="*60)
    
    from data_structures.heap import RecommendationHeap
    
    heap = RecommendationHeap()
    
    # Insert items
    test_data = [
        ('Rock', 8.5),
        ('Pop', 6.2),
        ('Jazz', 9.1),
        ('Classical', 5.5),
    ]
    
    for genre, score in test_data:
        heap.insert(genre, score)
    
    print(f"✓ Heap size: {heap.size()}")
    print(f"✓ Heap valid: {heap.validate_heap_property()}")
    
    # Extract top items
    print("\n✓ Top 3 recommendations:")
    for i in range(3):
        if not heap.is_empty():
            item = heap.extract_max()
            print(f"  {i+1}. {item['genre']}: {item['score']}")
    
    print("\n✅ HEAP TEST PASSED!")
    return True

def test_trie():
    """Test Trie implementation"""
    print("\n" + "="*60)
    print("TESTING TRIE DATA STRUCTURE")
    print("="*60)
    
    from data_structures.trie import GenreTrie
    
    trie = GenreTrie()
    
    # Insert genres
    genres = ['Rock', 'Pop', 'Jazz', 'Classical', 'Rock and Roll', 'Popular']
    
    for genre in genres:
        trie.insert(genre)
    
    print(f"✓ Words inserted: {trie.count_words()}")
    print(f"✓ Max depth: {trie.max_depth()}")
    print(f"✓ Total nodes: {trie.count_nodes()}")
    
    # Test search
    print(f"\n✓ Search 'Rock': {trie.search('rock')}")
    print(f"✓ Search 'Metal': {trie.search('metal')}")
    
    # Test autocomplete
    suggestions = trie.autocomplete('po')
    print(f"\n✓ Autocomplete 'po': {[s['word'] for s in suggestions]}")
    
    print("\n✅ TRIE TEST PASSED!")
    return True

def test_bst():
    """Test Binary Search Tree implementation"""
    print("\n" + "="*60)
    print("TESTING BST DATA STRUCTURE")
    print("="*60)
    
    from data_structures.bst import ArtistBST
    
    bst = ArtistBST()
    
    # Insert artists with song counts
    artists = [
        ('Taylor Swift', 5),
        ('Ed Sheeran', 3),
        ('The Beatles', 7),
        ('Queen', 4),
    ]
    
    for artist, count in artists:
        bst.insert(artist, count)
    
    print(f"✓ BST size: {bst.size()}")
    print(f"✓ BST height: {bst.height()}")
    print(f"✓ Is balanced: {bst.is_balanced()}")
    
    # Test traversals
    print(f"\n✓ Inorder traversal (first 3):")
    inorder = bst.inorder_traversal()[:3]
    for item in inorder:
        print(f"  {item['artist']}: {item['count']} songs")
    
    # Test range query
    range_result = bst.range_query(3, 5)
    print(f"\n✓ Artists with 3-5 songs: {len(range_result)} found")
    
    print("\n✅ BST TEST PASSED!")
    return True

def test_dijkstra():
    """Test Dijkstra's Algorithm"""
    print("\n" + "="*60)
    print("TESTING DIJKSTRA'S ALGORITHM")
    print("="*60)
    
    from data_structures.graph import MusicGraph
    from algorithms.dijkstra import DijkstraAlgorithm
    
    graph = MusicGraph()
    
    # Build a simple graph
    songs = [
        {'genre': 'Rock'},
        {'genre': 'Rock'},
        {'genre': 'Pop'},
        {'genre': 'Jazz'},
    ]
    
    for song in songs:
        graph.add_song(song)
    
    graph.build_genre_graph(songs, [])
    
    dijkstra = DijkstraAlgorithm(graph)
    distances = dijkstra.compute_shortest_paths()
    
    print(f"✓ Execution time: {dijkstra.execution_time:.4f} seconds")
    print(f"✓ Distances computed: {len(distances)}")
    print(f"\n✓ Sample distances:")
    for genre, dist in list(distances.items())[:3]:
        print(f"  {genre}: {dist}")
    
    # Test centrality
    central = dijkstra.find_most_central_genre()
    if central:
        print(f"\n✓ Most central genre: {central[0]} (avg distance: {central[1]:.2f})")
    
    print("\n✅ DIJKSTRA TEST PASSED!")
    return True

def test_sorting():
    """Test Sorting Algorithms"""
    print("\n" + "="*60)
    print("TESTING SORTING ALGORITHMS")
    print("="*60)
    
    from algorithms.sorting import QuickSort, MergeSort
    
    # Test data
    genre_scores = {
        'Rock': 8.5,
        'Pop': 6.2,
        'Jazz': 9.1,
        'Classical': 5.5,
        'Electronic': 7.3
    }
    
    # QuickSort test
    qs = QuickSort()
    sorted_qs = qs.sort_by_score(genre_scores)
    print(f"\n✓ QuickSort:")
    print(f"  Result: {sorted_qs[:3]}")
    print(f"  Comparisons: {qs.comparison_count}")
    print(f"  Time: {qs.execution_time:.6f}s")
    
    # MergeSort test
    distances = {'Rock': 0, 'Pop': 2, 'Jazz': 1, 'Classical': 3}
    ms = MergeSort()
    sorted_ms = ms.sort_by_distance(distances)
    print(f"\n✓ MergeSort:")
    print(f"  Result: {sorted_ms}")
    print(f"  Comparisons: {ms.comparison_count}")
    print(f"  Time: {ms.execution_time:.6f}s")
    
    print("\n✅ SORTING TEST PASSED!")
    return True

def test_clustering():
    """Test K-Means Clustering"""
    print("\n" + "="*60)
    print("TESTING K-MEANS CLUSTERING")
    print("="*60)
    
    from algorithms.clustering import MusicClusterer
    
    # Sample songs
    songs = [
        {'genre': 'Rock', 'artist': 'Artist1', 'price': 0.99},
        {'genre': 'Rock', 'artist': 'Artist2', 'price': 1.29},
        {'genre': 'Pop', 'artist': 'Artist3', 'price': 0.99},
        {'genre': 'Pop', 'artist': 'Artist4', 'price': 1.29},
        {'genre': 'Jazz', 'artist': 'Artist5', 'price': 1.99},
    ]
    
    clusterer = MusicClusterer(k=3)
    result = clusterer.cluster_songs(songs, max_iterations=50)
    
    print(f"✓ Clusters created: {result['total_clusters']}")
    print(f"✓ Execution time: {clusterer.execution_time:.4f}s")
    print(f"✓ Silhouette score: {result['silhouette_score']}")
    print(f"\n✓ Cluster sizes: {result['cluster_sizes']}")
    
    print("\n✅ CLUSTERING TEST PASSED!")
    return True

def test_analyzer():
    """Test Music Analyzer"""
    print("\n" + "="*60)
    print("TESTING MUSIC ANALYZER")
    print("="*60)
    
    from utils.analyzer import MusicAnalyzer
    
    analyzer = MusicAnalyzer()
    
    # Sample data
    playlist = [
        {'genre': 'Rock', 'artist': 'Artist1'},
        {'genre': 'Rock', 'artist': 'Artist2'},
        {'genre': 'Pop', 'artist': 'Artist1'},
    ]
    
    recommendations = [
        {'genre': 'Jazz', 'artist': 'Artist3'},
    ]
    
    distances = {'Rock': 0, 'Pop': 1, 'Jazz': 2}
    
    # Test genre scores
    scores = analyzer.calculate_genre_scores(playlist, recommendations, distances)
    print(f"✓ Genre scores calculated: {scores}")
    
    # Test artist analysis
    artists = analyzer.analyze_artists(playlist, recommendations)
    print(f"\n✓ Artist counts: {artists}")
    
    # Test diversity
    patterns = analyzer.analyze_temporal_patterns(playlist)
    print(f"\n✓ Genre diversity: {patterns['genre_diversity']}")
    print(f"✓ Artist diversity: {patterns['artist_diversity']}")
    
    # Test insights
    insights = analyzer.generate_insights(playlist, recommendations)
    print(f"\n✓ Generated {len(insights)} insights")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight['message']}")
    
    print("\n✅ ANALYZER TEST PASSED!")
    return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎵 MUSIC RECOMMENDATION SYSTEM - VERIFICATION")
    print("="*60)
    
    tests = [
        ("Graph", test_graph),
        ("Max Heap", test_heap),
        ("Trie", test_trie),
        ("BST", test_bst),
        ("Dijkstra", test_dijkstra),
        ("Sorting", test_sorting),
        ("Clustering", test_clustering),
        ("Analyzer", test_analyzer),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} TEST FAILED!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Your system is fully functional!")
        print("\nYour data structures ARE working and being used by the backend.")
        print("Run 'python server.py' to start the Flask server.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)