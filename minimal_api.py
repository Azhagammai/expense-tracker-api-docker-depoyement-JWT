from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Expense Tracker API is running!', 'status': 'success'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is operational'})

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'message': 'GET request successful',
            'data': {'test': True}
        })
    else:
        data = request.get_json() if request.is_json else {}
        return jsonify({
            'status': 'success',
            'message': 'POST request successful',
            'received_data': data
        })

if __name__ == '__main__':
    print("Starting Minimal Expense Tracker API...")
    print("Server will be available at: http://localhost:5000")
    print("Test endpoints:")
    print("  GET  http://localhost:5000/")
    print("  GET  http://localhost:5000/health") 
    print("  GET  http://localhost:5000/api/test")
    print("  POST http://localhost:5000/api/test")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
