from app import create_app  # Import the create_app function

# Call create_app to get the Flask app and MongoDB instance
app, mongo = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application
