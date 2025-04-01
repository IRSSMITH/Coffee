from search import app
import threading
import crawler

# Run crawler in background
threading.Thread(target=crawler.crawl, args=("https://en.wikipedia.org/wiki/Main_Page", 2)).start()

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)
