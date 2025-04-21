from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/roblox/game/details') 
def get_details():
    game_id = request.args.get('id')
    if not game_id:
        return Response(
            "Please provide a valid game ID.",
            status=400,
            mimetype='text/plain'
        )

    url = f"https://www.roblox.com/games/{game_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        image_meta = soup.find('meta', attrs={'property': 'og:image'})
        image_url = image_meta.get('content') if image_meta else None

        title_meta = soup.find('meta', attrs={'property': 'og:title'})
        title = title_meta.get('content') if title_meta else None

        data = {
            "success": {
                "title": title,
                "image": image_url
            }
        }

        return Response(
            json.dumps(data, ensure_ascii=False, indent=4),
            mimetype='application/json; charset=utf-8'
        )

    except requests.exceptions.RequestException as e:
        error_msg = f"Unable to fetch game ID, please try again later."
        return Response(error_msg, status=500, mimetype='text/plain')

    except Exception as e:
        error_msg = f"{e}"
        return Response(error_msg, status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
