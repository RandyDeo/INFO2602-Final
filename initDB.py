from main import app
from models import db, User

db.create_all(app=app)

bob = User(id="1", username="bob", email="bob@mail.com")
bob.set_password("bobpass")
db.session.add(bob)
db.session.commit()

print('database initialized!')