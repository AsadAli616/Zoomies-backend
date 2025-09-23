from app import create_app  # import the factory function

app = create_app()  # create the full Flask app with all blueprints

if __name__ == "__main__":
    app.run(debug=True)