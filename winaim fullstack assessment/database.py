from main2 import db, app

with app.app_context():
    db.create_all()
