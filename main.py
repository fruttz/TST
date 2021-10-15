from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json

with open("menu.json", "r") as read_file:
    data = json.load(read_file)

app = FastAPI()
menu = data["menu"]


class Item(BaseModel):
    id: int
    nama: str

@app.get("/")
async def root():
    return {"Home":"Home Page"}

@app.get("/menu")
async def read_menu():
    return menu

@app.post("/add-menu")
async def add_menu(name: str):
    id = 1
    if (len(menu) > 0):
        id = menu[len(menu)-1]['id']+1
    new_item = {'id':id, 'name':name}
    menu.append(dict(new_item))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    write_file.close()
    return new_item

@app.get("/get-menu/{id}")
async def get_menu(id: int):
    for menu_item in menu:
        if menu_item['id'] == id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.put("/update-menu/{id}")
async def update_menu(id: int, name: str):
    for menu_item in menu:
        if menu_item['id'] == id:
            menu_item['name'] = name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return {"message": "Item Updated Successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete("/del-menu/{id}")
async def delete_menu(id: int):
    for menu_item in menu:
        if menu_item['id'] == id:
            menu.remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return {"message": "Item Deleted Successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

