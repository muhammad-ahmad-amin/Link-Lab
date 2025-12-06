"""
Graph Data Structure - Adjacency List Implementation
Represents relationships between music genres
"""

from collections import defaultdict, Counter

class MusicGraph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.nodes = set()
        self.genre_counts = Counter()
        
    def add_node(self, node):
        """Add a genre node to the graph"""
        if node not in self.nodes:
            self.nodes.add(node)
            self.adjacency_list[node] = []
    
    def add_edge(self, from_node, to_node, weight):
        """Add a weighted edge between two genres"""
        self.add_node(from_node)
        self.add_node(to_node)
        
        # Check if edge already exists
        for edge in self.adjacency_list[from_node]:
            if edge['to'] == to_node:
                return
        
        self.adjacency_list[from_node].append({
            'to': to_node,
            'weight': weight
        })
    
    def add_song(self, song):
        """Add a song and update genre counts"""
        genre = song.get('genre')
        if genre:
            self.genre_counts[genre] += 1
            self.add_node(genre)
    
    def build_genre_graph(self, playlist, recommendations):
        """
        Build a complete weighted graph of genres
        Weight = 1 + |count_difference|
        """
        # Count genres from playlist (weight 1)
        for song in playlist:
            if song.get('genre'):
                self.genre_counts[song['genre']] += 1
        
        # Count genres from recommendations (weight 2)
        for song in recommendations:
            if song.get('genre'):
                self.genre_counts[song['genre']] += 2
        
        genres = list(self.genre_counts.keys())
        
        # Create complete graph with weighted edges
        for i in range(len(genres)):
            for j in range(i + 1, len(genres)):
                weight = 1 + abs(
                    self.genre_counts[genres[i]] - 
                    self.genre_counts[genres[j]]
                )
                
                self.add_edge(genres[i], genres[j], weight)
                self.add_edge(genres[j], genres[i], weight)
        
        return {
            'genre_counts': dict(self.genre_counts),
            'nodes': list(self.nodes),
            'edges': self._get_edges_list()
        }
    
    def _get_edges_list(self):
        """Get list of all edges"""
        edges = []
        processed = set()
        
        for node, neighbors in self.adjacency_list.items():
            for edge in neighbors:
                pair = tuple(sorted([node, edge['to']]))
                if pair not in processed:
                    edges.append({
                        'from': node,
                        'to': edge['to'],
                        'weight': edge['weight']
                    })
                    processed.add(pair)
        
        return edges
    
    def get_adjacency_list(self):
        """Get the adjacency list representation"""
        return dict(self.adjacency_list)
    
    def get_neighbors(self, node):
        """Get all neighbors of a node"""
        return self.adjacency_list.get(node, [])
    
    def node_count(self):
        """Get total number of nodes"""
        return len(self.nodes)
    
    def edge_count(self):
        """Get total number of edges"""
        count = 0
        for neighbors in self.adjacency_list.values():
            count += len(neighbors)
        return count // 2  # Divide by 2 for undirected graph
    
    def clear(self):
        """Clear the graph"""
        self.adjacency_list.clear()
        self.nodes.clear()
        self.genre_counts.clear()
    
    def get_graph_density(self):
        """Calculate graph density"""
        n = self.node_count()
        if n <= 1:
            return 0
        max_edges = n * (n - 1) / 2
        return self.edge_count() / max_edges if max_edges > 0 else 0
    
    def degree_distribution(self):
        """Get degree distribution of the graph"""
        degrees = {}
        for node in self.nodes:
            degree = len(self.adjacency_list[node])
            degrees[node] = degree
        return degrees
    
    def __str__(self):
        """String representation of the graph"""
        result = f"Graph with {self.node_count()} nodes and {self.edge_count()} edges\n"
        for node in sorted(self.nodes):
            neighbors = [f"{e['to']}({e['weight']})" for e in self.adjacency_list[node]]
            result += f"{node}: {', '.join(neighbors)}\n"
        return result