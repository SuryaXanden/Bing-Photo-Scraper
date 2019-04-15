import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

def finder(place_address):
    answer = {}
    
    answer['image_url'] = "No results found"

    url = r"https://www.bing.com/images/search?q={}&pq=".format(place_address, place_address)

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    with open("op.html",'wb') as f:
        data_to_write = soup.prettify()
        f.write(data_to_write.encode('utf-8'))

    try:
        image = soup.select_one("div > a > div > img")
        print(image['src'])
        answer['image_url'] = image['src']

    except Exception as e:
        print(e)
        answer['image_url'] = "No results found"

    return answer

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
    if request.args.get('q') and request.args.get('auth') == "lf":
        item = request.args.get('q').replace(" ",'+').replace("%20","+")
        return jsonify(finder(item))
    else:
        return jsonify({"error": "Use /?q=<address>&auth=<authorization>"})

app.run(debug=True, port=80, threaded=True)
