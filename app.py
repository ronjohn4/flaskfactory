from flaskfactory import create_app, db

if __name__ == "__main__":
    app = create_app()
    test_client = app.test_cl
    app.run(debug=True)
