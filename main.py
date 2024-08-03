from curses.ascii import GS
from enum import Enum
from unicodedata import category
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

items = {
    0: Item(name='Hammer', price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name='Pliers', price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name='Nails', price=1.99, count=20, id=2, category=Category.CONSUMABLES),
}

'''
FastAPI handles JSON serialization and deserialization for us.
We can simply use bult-in python and Pydantic types, in this case dict[int, Item]
'''
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
# def index():
    return {'items': items}

@app.get("/items/{item_id}")
def get_item(item_id:int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404)
    else:
        return items[item_id]

