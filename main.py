from flask import Flask, render_template, request, Response
import pytesseract
import re
from PIL import Image
import json

app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("upload.html")


@app.route('/extract_date', methods=['POST', 'GET'])
def extract_date():
    date = ""
    if request.method == 'POST':
        f = request.files['file']
        string2 = Image.open(f)

        text = pytesseract.image_to_string(string2)
        try:
            date = re.search(r'[Date:]*([0-9]{0,2}[\/-]([0-9]{0,2}|[A-Z]|[A-z]{3})[\/-][0-9]{0,4})', text).group(1)
        except AttributeError:
            date = 'Null'
        d = {"date": date}
        data = json.dumps(d)
        return Response(response=data, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080", debug=True)
