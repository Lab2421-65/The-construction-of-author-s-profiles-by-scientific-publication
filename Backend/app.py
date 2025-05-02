from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

from models import get_data, get_batch, get_closest, get_by_scopus_id

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/get_data")
def get_all():
    """
    :returns: list of all records
    """
    data = get_data()
    return data


@app.get("/api/get_author/{scopus_id}")
async def get_by_name(scopus_id: str):
    """
    :param : name of the person
    :returns: record
    """
    human = get_by_scopus_id(scopus_id)
    draw_Categories = []
    for key, value in human.get('Categories', {}).items():
        draw_Categories.append((key, value))
    draw_Categories.append(draw_Categories[0])
    human['draw_Categories'] = draw_Categories
    return human


@app.get("/api/get_closest/{scopus_id}")
async def get_closest_by_orcid(scopus_id: str, size: int=5):
    """
    :param ORCID: ORCID of the person
    :returns: list of records with the given name
    """
    closest = get_closest(scopus_id, top=size)
    return closest

@app.get("/api/paginate/{page}")
async def get_data_by_page(page: int=1, page_size: int = 10):
    """
    :param page: page number
    :param page_size: number of records per page
    :returns: list of records
    """
    data = get_batch(page, page_size)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
