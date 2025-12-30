from fastapi import FastAPI,Response,HTTPException,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db 


models.Base.metadata.create_all(bind = engine)

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True #defalt value
 
while True:

    try:
        conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user = 'postgres',password = "Lavanyarj@8",cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Connecting a database successfully")
        break
    except Exception as error: 
        print("Connecting a database failed")
        print("Error: ",error)
        time.sleep(2)

    
    
my_posts = [{"title" : "model1","content":"model performce","publish": True,"rating": 5 , "id": 1},
           {"title" : "model2","content":"model performce","publish": True,"rating": 5 , "id": 2},
           {"title" : "model3","content":"model performce","publish": True,"rating": 5 , "id": 3}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id :
            return post

def find_Post_By_Index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id : 
            return index


@app.get("/")
def health():
    return {"status": "connected"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts }

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts }


@app.post("/createPosts",status_code= status.HTTP_201_CREATED)
def create_post(post: Post,db: Session = Depends(get_db) ):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    
    # new_post= models.Post(title=post.title,content=post.content,published=post.published)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return { "data": new_post}

@app.get("/{id}",status_code = status.HTTP_404_NOT_FOUND)
def get_Post_By_Id( id : int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # test_post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail={ "message" : f"Post with a given id {id} is found"})
    else:
        return {"post_detail": post}
        
@app.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id :int,db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail={ "message" : f"Post with a given id {id} is found"})
    
    post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_Post(id : int, updated_post : Post,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s,content = %s,published = %s  WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))
    # updated_Post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail={ "message" : f"Post with a given id {id} is found"})
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    
    return {"data": post_query.first()}

