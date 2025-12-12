### 🔗 Link-Lab: Graph-Based Recommendation System

**Link-Lab** is a **graph-based recommendation system** developed as part of our **Data Structures and Algorithms (DSA)** end-semester project. It’s designed to recommend **movies and other products** by modeling relationships between users, items, and preferences as a **graph network**.

#### 🧩 Key Features

* **Graph-Driven Recommendations:** Uses graph traversal and similarity measures to generate intelligent suggestions across multiple domains (e.g., movies, songs, products, etc.).
* **Efficient DSA Implementation:** Core recommendation logic built using fundamental data structures — graphs, heaps, hash maps, and trees.
* **Scalable Architecture:** Designed to easily extend for new datasets and recommendation types.
* **Visualization Support:** Displays relationships and recommendation paths through interactive or visual graph components.

#### 🧠 Technical Highlights

* **Language:** Python, JS, HTML, CSS
* **Algorithms:** BFS, DFS, Dijkstra’s Algorithm, PageRank-style ranking, collaborative filtering concepts
* **Core Idea:** Represent users and items as nodes in a graph, and generate recommendations by exploring their connections and similarities.

#### 🎓 Project Context

Developed as a **DSA end-semester project** to demonstrate the real-world application of data structures and algorithms in building intelligent and efficient recommendation systems.

---

## 🚀 How to Run the Project

To run Link-Lab locally, follow these steps:

### **1️⃣ Install Dependencies**

Make sure you have **Python 3** installed.

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

### **2️⃣ Start Backend Servers**

You must run **all three Python recommendation servers** in **separate terminals**.

#### **Terminal 1 — Shopping Recommendations**

```bash
python ./backend/shopping_recommendations.py
```

#### **Terminal 2 — Songs Recommendations**

```bash
python ./backend/songs_recommendations.py
```

#### **Terminal 3 — Movies Recommendations**

```bash
python ./backend/movies_recommendations.py
```

All three servers must be running simultaneously.

---

### **3️⃣ Start Frontend**

After starting all servers, simply open:

```
index.html
```

in your browser (just double-click it).

This will load the UI and connect to the running backend servers.

---

### ✅ You're Ready!
