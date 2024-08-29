from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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

new_df = movies[['id','title','tags']]
print(new_df.head())
    
new_df.loc[:, 'tags'] = new_df['tags'].fillna('')
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(new_df['tags'].fillna(''))
print("cv done")

similarity_matrix = cosine_similarity(X)
print("sim done")

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/recommend/{title}")
def recommend(title:str):
    idx = new_df[new_df['title'] == title].index[0]
    dist=sorted(list(enumerate(similarity_matrix[idx])),reverse=True,key=lambda vec:vec[1])
    recommended_movies = []
    for i in dist[1:6]:
        recommended_movies.append(new_df.iloc[i[0]]['title'])
    return {"recommended_movies": recommended_movies}



@app.get("/check/{title}")
def check(title:str):
    overview = movies.loc[movies['title'] == title, 'overview'].values
    genre = movies.loc[movies['title'] == title, 'genres'].values
    tag = movies.loc[movies['title'] == title, 'tags'].values
    print(movies.head())


    


    print(new_df[new_df['title'] == 'The Shawshank Redemption'])

    #idx = movie_index[movie_title]
    index = new_df[new_df['title'] == movies].index[0]
    print(index)
    dist=sorted(list(enumerate(similarity_matrix[index])),reverse=True,key=lambda x:x[1])
    print(dist)
    for i in dist[1:6]:
        print(new_df.iloc[i[0]])

    
    if len(overview) > 0:
        return overview[0], genre[0], tag[0]
    else:
        return "Title not found."


    # similarity_scores = list(enumerate(similarity_matrix[index]))
    # similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    # movie_indices = [i[0] for i in similarity_scores[1:6]]  # Top 5 recommendations

    # recommended_movies =new_df.iloc[movie_indices]['title'].tolist()
    # return {"recommended_movies": recommended_movies}
    #dist=sorted(list(enumerate(sim[0])),reverse=True,key=lambda vec:vec[1])
    # print(dist[1:6])
    # for i in dist[1:6]:
    #     print(i)
    #     print(new_df.iloc[i[0]].title)
    
    # def recommend(title:str):
    #     idx = new_df[new_df['title'] == movies].index[0]
    #     dist=sorted(list(enumerate(sim[idx])),reverse=True,key=lambda vec:vec[1])
    #     for i in dist[1:6]:
    #         print(new_df.iloc[i[0]])