from flask import Flask, render_template, request
from qrkit.qrimg import encode_to_img

from io import BytesIO
import base64

app = Flask(__name__)

import qrcode


def png_base64_image(content):
    img = qrcode.make(content)

    with BytesIO() as f:
        img.save(f, "PNG", quality=80)
        imgb64 = base64.b64encode(f.getvalue()).decode('utf-8')

    return imgb64


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/url/")
def url():
    return render_template('url.html')

@app.route("/url/", methods=['POST'])
def url_qrcode():
    url = request.form.get("url")

    imgb64 = png_base64_image(url)
    return render_template('qrimage.html', imgb64=imgb64, url=url)


@app.route("/qrwifi/", methods=['POST'])
def qrwifi():
    try:
        ssid = request.form.get("ssid")
        passwd = request.form.get('passwd')
        stype = request.form.get('stype', 'WEP')
    except Exception as e:
        raise

    if stype.lower() == 'wpa':
        stype = 'WPA'
    else:
        stype = 'WEP'

    imgb64 = png_base64_image("WIFI:S:{};T:{};P:{};;".format(ssid, stype, passwd))
    return render_template('qrimage-wifi.html', imgb64=imgb64, ssid=ssid)

if __name__ == "__main__":
    app.run(debug=True)
