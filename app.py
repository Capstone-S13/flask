from application import create_app, db

if __name__== "__main__":
    app = create_app()
    # print(app.url_map)
    app.run(host="0.0.0.0",port=3000)
