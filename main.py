from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    @app.route('/')
    def landing_page():
        return "Hello World"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
