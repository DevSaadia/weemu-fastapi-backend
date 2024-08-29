from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

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

df = pd.read_csv('archive/movies_metadata.csv', low_memory=False)
df = df[['title','overview']]

# df = pd.read_csv('archive/movies_metadata.csv')

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/data/{query}")
def query_data(query: str):
    # Perform some operation using the dataset and the query
    return df.head()
    # result = df[df['column_name'].str.contains(query, na=False)]
    # # Convert the result to a dictionary
    # result_dict = result.to_dict(orient='records')
    # return {"result": result_dict}

@app.get("/check/{title}")
def check(title:str):
    overview = df.loc[df['title'] == title, 'overview'].values
    if len(overview) > 0:
        return overview[0]
    else:
        return "Title not found."
