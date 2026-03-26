from flask import Flask, render_template
from routes.api import api_bp

app = Flask(__name__)

# Registrar módulos
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)