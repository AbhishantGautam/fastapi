from sys import prefix
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from fastapi.params import Body
import random


router = APIRouter(
    prefix = '/posts',
    tags = ['posts']
)

@router.get('/', response_model=List[schemas.Post_new]) #the response from api is list of dictionary, we only need dictionary, 'List' function extracts the list elements
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int = 10, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).all()
    #to search for abhishant gautam in the title, write ?search=abhishant%20gautam. because %20 represents a spacebar in the url
    # db.query(models.Post) --> the actual sql query (ie : select * from posts)

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    return posts


# if two path operations refer to the same path, the one written first will get executed

#sample data:
my_posts = [
    {
        "title":"title1", "content":"content1", "id":1
    },
    {
        "title":"title2", "content":"content2", "id":2
    },
]

# @router.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print(payload)
#     return {"new post" : f"title:{payload['title']}, content:{payload['content']}"}

# @router.post('/createpost', status_code=status.HTTP_201_CREATED) #status_code changes the default http response code to the desired response code
# def create_post(new_post : schemas.Post): #stating that input to this post request must replicate the Post data model we created earlier
#     post_dict = new_post.dict() # Here the new_post is a pydantic model (ie : inherited from pydantic's BaseModel). And every pydantic model has a .dict() method which converts the pydantic BaseModel object to dictionary
#     post_dict['id'] = random.randrange(0,1000000)
#     my_posts.append(post_dict)
#     return {"data" : post_dict}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post_new)
def create_posts(post:schemas.Post, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) #creating a table row object
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # instead of above line, we can also write this line, where we unpacked a dictionary and auto assigned values.
    db.add(new_post) #adding that row to the table
    db.commit() #commiting the change to the actual database
    db.refresh(new_post) #stores the newly created row object in a newly created variable 'new_post'


    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    return new_post

def post_frm_id(id):
    for item in my_posts:
        if item['id'] == id:
            return item

@router.get('/{id}') #id--> path parameter --> will always be rendered as string. So first we need to typecast it or validate it.
def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):#validated the id to always be an integer

    # # post = post_frm_id(id)
    # cursor.execute("""select * from posts where id=%s""",(str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    #now if some invalid id is entered, the server will just say no value found, but with a response http response code of 200(ie: all went well). If we want it to return some error in the form of http status code, do following:
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND # this will give 404 error whenever an id is inputted which is not there in our dataset
        # return {"message" : f"post with id={id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'not authorized to perform the action')
    return {"data" : post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not authorized to perform operation')
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id) #finds the index position of the post in the posts list with id= 'id of the post to be deleted'
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # my_posts.pop(index)
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post_new)
def update_post(id: int, post: schemas.Post, db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning *""",(post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_one = post_query.first()

    if post_one == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id ={id} not found')

    if post_one.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'not authorized to perform the action')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f'post with id = {id} does not exist')

    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id ={id} not found')

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()
