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

original_items = {
    0: Item(name='Hammer', price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name='Pliers', price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name='Nails', price=1.99, count=20, id=2, category=Category.CONSUMABLES),
}
items = original_items.copy()

'''
FastAPI handles JSON serialization and deserialization for us.
We can simply use bult-in python and Pydantic types, in this case dict[int, Item]
'''
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
# def index():
    return {'items': items}

@app.get("/items/{item_id}")
def query_item_by_item_id(item_id:int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404)
    else:
        return items[item_id]

# helper type/alias: python 3.10+
Selection = dict[
    str, str|int|float|Category|None
]

@app.get("/items/")
def query_items_by_parameters(
    name: str|None=None,
    price: float|None=None,
    count: int|None=None,
    category: Category|None=None
# ) -> dict[str, Selection]: # error
) -> dict[str, Selection|list[Item]]:
    def check_item(item:Item) -> bool:
        return all(
            (            
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            )        
        )
    
    selection = [item for item in items.values() if check_item(item)]
    return {
        'query': dict(name=name, price=price, count=count, category=category),
        'selection': selection
    }

@app.get('/reset')
def add_item() -> dict[str, dict]:
    global items
    items = original_items.copy()
    return {'reset': items}

@app.post('/')
def add_item(item:Item) -> dict[str, Item]:
    
    if item.id  in items:
        raise HTTPException(status_code=400, detail=f'{item.id=} already exists')

    items[item.id] = item
    return {'added': item}

@app.put('/update/{item_id}')
def update(
        item_id: int,
        name: str|None=None,
        price: float|None=None,
        count: int|None=None,
        # category: Category|None=None
# ) -> dict[str, Item]:
) -> dict:
    params = {k:v for k,v in locals().items() 
              if v is not None and k != 'item_id'}
    # return params

    if item_id not in items:
        raise HTTPException(status_code=404)

    if all(info is None for info in (name, price, count)):
        raise HTTPException(status_code=400, 
                            detail='no parameters')
    item = items[item_id]
    for k, v in params.items():
        setattr(item, k, v)
    return {'updated': item}