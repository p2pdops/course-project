import os
from flask import Flask, render_template

import auth
import admin

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join('data', 'database.sqlite'),
)

app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)


@app.route('/')
@auth.login_required
def hello():
    return render_template('base.html')


app.run(host='0.0.0.0', port=3000, debug=True)
