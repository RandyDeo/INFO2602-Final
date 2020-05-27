from main import app
from models import db, User, Post

db.create_all(app=app)

bob = User(id="1", username="bob", email="bob@mail.com")
bob.set_password("bobpass")

alice = User(id="2", username="alice", email="alice@mail.com")
alice.set_password("alicepass")

db.session.add(bob)
db.session.add(alice)

db.session.commit()

post = Post(id="1",userid="1", text="This is the First Post")
db.session.add(post)
db.session.commit()

print('database initialized!')