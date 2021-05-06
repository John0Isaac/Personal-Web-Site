from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    @app.route("/")
    def landing_page():
        return "Hello World"

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
