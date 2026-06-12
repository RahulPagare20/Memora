from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from flask_cors import CORS, cross_origin
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.secret_key = "&@*)#%Ra%&hul_s46h6@7rin^%k1.0@%s5hr##ink^$#prot&o&&ty(@$p))(*e1$#^&point0!$%$^$"
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return 'Welcome to Memora'

port = 9999
if __name__ == "__main__":
    app.run(port=port)