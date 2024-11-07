from flask import Flask, request, redirect
import random
import string
from urllib.parse import urlparse

# Initialize the Flask app
app = Flask(__name__)

# In-memory dictionary for URL mapping (temporary storage)
url_mapping = {}

# Function to generate a random short URL (6 characters long by default)
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Validate the URL format (check if it's a valid URL)
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # http:// or https://
    except ValueError:
        return False

# Route to shorten a URL (Input the original URL as a query parameter)
@app.route('/shorten')
def shorten_url():
    original_url = request.args.get('url')
    length = int(request.args.get('length', 6))  # Optional: specify length via query parameter

    # Validate the provided URL
    if not original_url or not is_valid_url(original_url):
        return "Please provide a valid URL", 400

    # Generate a new short URL and store the mapping
    short_url = generate_short_url(length)
    url_mapping[short_url] = original_url

    return f"Shortened URL: /{short_url}"

# Redirect route: When the user visits a short URL, redirect to the original URL
@app.route('/<short_url>')
def redirect_to_url(short_url):
    # Look up the original URL from the dictionary
    original_url = url_mapping.get(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found", 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)