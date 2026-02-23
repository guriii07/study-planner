from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # This automatically creates your SQLite database the first time you run the app
    with app.app_context():
        db.create_all() 
    
    app.run(debug=True, port=5000)