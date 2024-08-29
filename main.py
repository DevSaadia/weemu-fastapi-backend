from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

origins=[
    "http://localhost:3000",
    "https://weemu-fastapi-backend-00695719a2e1.herokuapp.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def extract_genre_names(genres):
    genres_list = json.loads(genres.replace("'", '"'))
    return " ".join([genre['name'] for genre in genres_list])
                                          
movies = pd.read_csv('archive/movies_metadata.csv', low_memory=False)
movies = movies[['id','title','overview','genres']]
movies['tags'] = movies['overview']+" "+movies['genres'].apply(extract_genre_names)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/check/{title}")
def check(title:str):
    overview = movies.loc[movies['title'] == title, 'overview'].values
    genre = movies.loc[movies['title'] == title, 'genres'].values
    tag = movies.loc[movies['title'] == title, 'tags'].values
    print(movies.head())
    new_df = movies[['id','title','tags']]
    print(new_df.head())
    
    new_df.loc[:, 'tags'] = new_df['tags'].fillna('')
    
    cv=CountVectorizer(max_features=10000, stop_words='english')
    print("cv done")
    # vec = cv.fit_transform(new_df['tags']).values.astype('U').toarray()
    vec = cv.fit_transform(new_df['tags']).toarray().astype('U')
    sim = cosine_similarity(vec)
    print("sim done")
    print(new_df[new_df['title'] == 'The Shawshank Redemption'])
    
    
    if len(overview) > 0:
        return overview[0], genre[0], tag[0]
    else:
        return "Title not found."
