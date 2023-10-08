from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/book', methods=['POST'])
def book_hotel():
    hotel_details = request.json
    return jsonify({"status": "success", "booking_id": 2})

@app.route('/cancel', methods=['POST'])
def cancel_hotel():
    booking_id = request.json.get('booking_id')
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(port=5002)
