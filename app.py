from application import create_app

if __name__== "__main__":
    app = create_app('flask.cfg')
    app.run(debug=True)