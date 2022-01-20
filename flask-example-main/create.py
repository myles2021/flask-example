from application import db
from application.models import Post

db.drop_all()
db.create_all()

