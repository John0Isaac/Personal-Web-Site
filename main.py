from flask import Flask, request, render_template
from flask_cors import CORS


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route("/")
    def landing_page():
        return render_template('pages/index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
