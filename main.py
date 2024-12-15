"""Работа с базой данных SQLite"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

# Добавление
user1 = User(username="kirill1", email="kirill1@example.com", password="12345")
user2 = User(username="kirill2", email="kirill2@example.com", password="12345")
# session.add_all([user1, user2])
# session.commit()

user1 = session.query(User).filter(User.username == "kirill1").first()
user2 = session.query(User).filter(User.username == "kirill2").first()

post1 = Post(title="My First Post", content="This is the content of the first post.", user_id=user1.id)
post2 = Post(title="Another Post", content="Content of another post.", user_id=user2.id)
post3 = Post(title="Another Postееееееееееее", content="Content of another post.", user_id=user2.id)
session.add_all([post1, post2, post3])
session.commit()

# Запросы
users = session.query(User).all()
for user in users:
    print(user.username, user.email)

posts = session.query(Post).join(User).all()
for post in posts:
    print(post.title, post.user.username)

user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
for post in user_posts:
    print(post.title)

# Обновление
user_to_update = session.query(User).filter(User.username == "kirill1").first()
user_to_update.email = "kirill_new@example.com"
session.commit()

post_to_update = session.query(Post).filter(Post.id == 1).first()
post_to_update.content = "Updated content for the first post."
session.commit()

# Удаление
post_to_delete = session.query(Post).filter(Post.id == 1).first()
session.delete(post_to_delete)
session.commit()

user_to_delete = session.query(User).filter(User.username == "kirill2").first()
session.delete(user_to_delete)
session.commit()
