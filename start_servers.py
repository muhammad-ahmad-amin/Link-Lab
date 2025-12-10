import subprocess
import sys
import os
import time

BACKEND = os.path.join(os.path.dirname(__file__), "backend")

def run(script, port):
    return subprocess.Popen(
        [sys.executable, script, "--port", str(port)],
        cwd=BACKEND
    )

if __name__ == "__main__":
    print("\n🚀 Starting music & songs servers...\n")

    music = run("movies_recommendations.py", 5000)
    time.sleep(1)

    songs = run("songs_recommendations.py", 5001)
    time.sleep(1)

    print("🎧 movies_recommendations -> http://localhost:5000")
    print("🎶 songs_recommendations -> http://localhost:5001")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        music.terminate()
        songs.terminate()
        print("\n🛑 Servers stopped.")