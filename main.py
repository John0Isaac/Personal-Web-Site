from flask import Flask, request, render_template, redirect, abort, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from models import setup_db, Diaries
from sqlalchemy import or_


RESULT_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULT_PER_PAGE
    end = start + RESULT_PER_PAGE

    results = [result.format() for result in selection]
    current_results = results[start:end]

    return current_results


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
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

    @app.route("/diaries")
    def retrieve_diaries():
        diaries = Diaries.query.order_by(Diaries.id).all()
        current_diaries = paginate_results(request, diaries)

        if len(current_diaries) == 0:
            abort(404)
        return jsonify({
            'sucess': True,
            'diaries': current_diaries,
            'total_diaries': len(Diaries.query.all())
        }), 200
        
    @app.route("/diary/<int:id>")
    def retrieve_diary(id):
            diary = Diaries.query.get(id)
            if not diary:
                abort(404)
            return jsonify({
                'sucess': True,
                'diary': diary.format()
            }), 200

    @app.route("/diaries", methods=['POST'])
    def add_diary():
        current_time = datetime.now(timezone.utc)
        try:
            new_title = request.form['title']
            new_category = request.form['category']
            new_content = request.form['content']
            new_date = current_time
            new_feeling = request.form['feeling']

            diary = Diaries(title=new_title, category=new_category, content=new_content, date=new_date, feeling=new_feeling)
            diary.insert()
            return jsonify({
                'sucess': True,
                'diary': diary.format()
            }), 200
        except:
            abort(422)
    
    @app.route("/diary/<int:id>", methods=['PATCH'])
    def edit_diary(id):
        diary = Diaries.query.get(id)
        if not diary:
            abort(404)
        try:
            new_title = request.form['title']
            new_category = request.form['category']
            new_content = request.form['content']
            new_feeling = request.form['feeling']
            
            diary.title = new_title
            diary.category = new_category
            diary.content = new_content
            diary.feeling = new_feeling
            
            diary.update()
            return jsonify({
                'sucess': True,
                'diary': diary.id
            }), 200
        except:
            abort(405)
    
    @app.route("/diary/<int:id>", methods=['DELETE'])
    def delete_diary(id):
        diary = Diaries.query.get(id)
        if diary:
            diary.delete()

            return jsonify({
            'sucess': True,
            'delete': id
        }), 200
        else:
            abort(404)
    
    @app.route('/diaries/search', methods=['POST'])
    def search_diaries():
        term = request.form.get('search_term')
        search = "%{}%".format(term.lower())
        diaries = Diaries.query.order_by(Diaries.id).filter(or_(Diaries.title.ilike(search),Diaries.category.ilike(search), Diaries.content.ilike(search) ))
        current_diaries = paginate_results(request, diaries)
        return jsonify({
            'sucess': True,
            'diries': current_diaries,
            'total_diaries': len(diaries.all())
            }), 200
    
    @app.route("/resume")
    def resume_page():
        return render_template('pages/resume.html')
    
    @app.route("/facebook")
    def facebook_link():
        return redirect("https://www.facebook.com/john0isaac")
    
    @app.route("/github")
    def github_link():
        return redirect("https://github.com/John0Isaac")
    
    @app.route("/linkedin")
    def linkedin_link():
        return redirect("https://www.linkedin.com/in/john0isaac")
    
    @app.route("/twitter")
    def twitter_link():
        return redirect("https://twitter.com/john00isaac")
    
    @app.route("/instagram")
    def instagram_link():
        return redirect("https://www.instagram.com/john0isaac")
    
    @app.route("/youtube")
    def youtube_link():
        return redirect("https://www.youtube.com/channel/UCJwxtw-l_nibkU54ZbVW8xw")

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resourse not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server errors'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
