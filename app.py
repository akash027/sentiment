
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Lambda function endpoint URL
LAMBDA_ENDPOINT = "https://9pzlrsonu7.execute-api.us-west-2.amazonaws.com/prod"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the review text from the request
    review = request.json.get('body')

    # Check if the review text exists
    if not review:
        return jsonify({'error': 'Review text is required!'}), 400

    try:
        print("Review received:", review)  # Debugging line

        # Forward the review to the Lambda function
        response = requests.post(LAMBDA_ENDPOINT, json={'body': review})
        response.raise_for_status()

        lambda_response = response.json()  # Parse the JSON response from Lambda
        print("Lambda response:", lambda_response)  # Debugging line

        # Return the parsed response as a proper JSON object
        return jsonify(lambda_response)
    except requests.exceptions.RequestException as e:
        print("Error while connecting to Lambda:", str(e))  # Debugging line
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)
