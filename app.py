from flask import Flask, request, send_file, render_template
from datetime import datetime
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os

from image_functions import generate_image, save_image

app = Flask(__name__)

print("##### Something is in fact happening!")

rt = os.getenv("APP_ROOT")
rt = rt if rt else ""
app.config["APPLICATION_ROOT"] = rt


@app.route("/")
def test_new_image():
    print("Ghooba looba")
    return render_template("test.html")


@app.route("/new", methods=["GET"])
def new_image():
    t = request.args.get(key="text")
    f_download = True if request.args.get(key="dl", default=1, type=int) != 0 else False
    if not t:
        t = request.form.get(key="text")
        f_download = (
            True if request.form.get(key="dl", default=1, type=int) != 0 else False
        )
    if not t:
        t = "<<<No text provided, here's some sample text>>"

    gen_image = generate_image(text=t)

    ts = datetime.now().timestamp().__str__()
    tss = ts.replace(".", "-")

    f_name = "new_image_" + tss + ".png"

    image_path = save_image(i=gen_image, file_name=f_name)

    r = send_file(
        path_or_file=image_path,
        mimetype="image/png",
        as_attachment=f_download,
        download_name=f_name,
        conditional=True,
        etag=True,
        last_modified=None,
        max_age=None,
    )
    return r


# Leftover from Replit:
# app.run(host='0.0.0.0', port=81, debug=False)

app.wsgi_app = DispatcherMiddleware(app, {app.config["APPLICATION_ROOT"]: app.wsgi_app})

if __name__ == "__main__":
    app.run(debug=False)
