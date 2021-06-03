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

    @app.route("/about")
    def about_page():
        return render_template('pages/about.html')

    @app.route("/blogs")
    def blogs_page():
        return render_template('pages/blogs.html')

    @app.route("/talks")
    def talks_page():
        return render_template('pages/talks.html')

    @app.route("/uses")
    def uses_page():
        return render_template('pages/uses.html')

    @app.route("/resume")
    def resume_page():
        return render_template('pages/resume.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
