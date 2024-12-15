﻿from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models import User, Post, SessionLocal

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users/list.html", {"request": request, "users": users})


@app.get("/users/create/")
def create_user_form(request: Request):
    return templates.TemplateResponse("users/form.html", {"request": request, "title": "Добавить пользователя", "user": None,
                                                          "url": "/users/create/"})


@app.post("/users/create/")
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...),
                db: Session = Depends(get_db)):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/users/{user_id}/edit/")
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users/form.html", {"request": request, "title": "Изменить пользователя", "user": user,
                                                          "url": f"/users/{user_id}/edit/"})


@app.post("/users/{user_id}/edit/")
def edit_user(user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...),
              db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/users/{user_id}/delete/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/posts/")
def list_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts/list.html", {"request": request, "posts": posts})


@app.get("/posts/create/")
def create_post_form(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("posts/form.html",
                                      {"request": request, "title": "Добавить пост", "post": None, "users": users,
                                       "url": "/posts/create/"})


@app.post("/posts/create/")
def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...),
                db: Session = Depends(get_db)):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    return RedirectResponse(url="/posts/", status_code=303)


@app.get("/posts/{post_id}/edit/")
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    users = db.query(User).all()
    return templates.TemplateResponse("posts/form.html",
                                      {"request": request, "title": "Изменить пост", "post": post, "users": users,
                                       "url": f"/posts/{post_id}/edit/"})


@app.post("/posts/{post_id}/edit/")
def edit_post(post_id: int, title: str = Form(...), content: str = Form(...), user_id: int = Form(...),
              db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    post.user_id = user_id
    db.commit()
    return RedirectResponse(url="/posts/", status_code=303)


@app.get("/posts/{post_id}/delete/")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/posts/", status_code=303)