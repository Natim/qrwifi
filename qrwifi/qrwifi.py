from flask import Flask, render_template, request
from qrkit.qrimg import encode_to_img

from io import BytesIO
import base64

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


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

    img = encode_to_img(("WIFI:S:{};T:{};P:{};;".format(ssid, stype, passwd)).encode('utf-8'),
                        500, 20)
    f = BytesIO()
    img.save(f, "PNG", quality=80)
    imgb64 = base64.b64encode(f.getvalue()).decode('utf-8')
    f.close()

    return render_template('qrimage.html', imgb64=imgb64, ssid=ssid)

if __name__ == "__main__":
    app.run(debug=True)
