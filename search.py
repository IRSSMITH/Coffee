from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def search(query):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT url, title FROM pages WHERE content LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    
    conn.close()
    return results

@app.route("/search", methods=["GET"])
def search_api():
    query = request.args.get("q", "")
    results = search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
