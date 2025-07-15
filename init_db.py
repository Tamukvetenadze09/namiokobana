from extensions import app, db
from models import User
from werkzeug.security import generate_password_hash
from models import Word

with app.app_context():
    db.drop_all()
    db.create_all()
    hashed_password = generate_password_hash("your_password_here")

    admin_user = User(
        username="admin",
        email="admin@example.com",
        password=hashed_password,
        role="Admin"
    )

    db.session.add(admin_user)
    db.session.commit()

    print("Database initialized and admin user created.")

    with app.app_context():
        db.create_all()
        print("✅ ცხრილები შეიქმნა")



