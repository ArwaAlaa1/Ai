from flask import Flask, request, jsonify
import wikipedia

app = Flask(__name__)

@app.route('/search_and_summary', methods=['GET'])
def search_and_summary():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        summary = wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return jsonify({"error": "Disambiguation error", "options": e.options}), 400
    except wikipedia.exceptions.PageError:
        return jsonify({"error": "Page not found"}), 404

    results = wikipedia.search(query)
    search_results = [{"index": i, "title": result} for i, result in enumerate(results)]

    response = {
        "summary": summary,
        "search_results": search_results
    }

    return jsonify(response)

@app.route('/page', methods=['GET'])
def get_page():
    subno = request.args.get('subno', type=int)
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = wikipedia.search(query)
    if subno is None or subno < 0 or subno >= len(results):
        return jsonify({"error": "Invalid subject number"}), 400

    try:
        page = wikipedia.page(results[subno])
        response = {
            "title": page.title,
            "content": page.content
        }
    except wikipedia.exceptions.DisambiguationError as e:
        response = {"error": "Disambiguation error", "options": e.options}
    except wikipedia.exceptions.PageError:
        response = {"error": "Page not found"}

    return jsonify(response)

if __name__ == '__main__':
    app.run()  # Note: app.run() is fine for development but we'll use Gunicorn for production
