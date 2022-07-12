from fastapi import FastAPI, Path

from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    color: Optional[str] = None

inventory = {
    1: {
        'name': 'Milk',
        'price': 3.99,
        'color': 'white'
    }
}

app = FastAPI()

@app.get('/')
async def home():
    return [1,'a','3']#{"Welcome": "Home Python"}

@app.get("/items/{item_id}")
async def get_item(item_id:int = Path(None, description="This is item get method")):
    return inventory[item_id]

@app.post('/create-items/{item_id}')
async def create_item(item_id:int, item: Item):
    if item_id in inventory:
        return "Item already exists"
    else:
        inventory[item_id] = item
        return inventory[item_id]

