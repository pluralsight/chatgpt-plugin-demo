# Import the libraries we need
import requests
from flask import Flask, request, send_from_directory

# Replace "YOUR_API_KEY_HERE" with your actual API key
# Even better, use best practices and store it as a secret (not hard-coded!)
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://www.alphavantage.co/query"

# Initialize the Flask app
app = Flask(__name__)


# When a user loads the home page, display 'Hello World!'
# This is not required for the plugin, but makes it easier to see that things are working when we deploy and test
@app.route("/")
def index():
  return "Hello world!  Your web application is working!"


# This route contains the core functionality to get stock information.  This calls the "Quote Endpoint" API from Alpha Vantage: https://www.alphavantage.co/documentation/#latestprice
@app.route('/stock', methods=['GET'])
def get_stock_data():
  symbol = request.args.get('symbol')

  params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": API_KEY}

  response = requests.get(BASE_URL, params=params)
  return response.json()


# ChatGPT will use this route to find our manifest file, ai-plugin.json; it will look in the "".well-known" folder
@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


# ChatGPT will use this route to find our API specification, openapi.yaml
@app.route('/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


# OPTIONAL: If you want a logo to display on your plugin in the Plugin Store, then upload a file named logo.png to the root of your project, and uncomment the code below.
@app.route('/logo.png')
def plugin_logo():
  return send_from_directory('.', 'logo.png')


# Run the app
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)