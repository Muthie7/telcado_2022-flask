from flask import Flask, request
import functools


class PermissionError(RuntimeError):
    pass

app = Flask(__name__)


stores = [
    {
        "name" : "Quickmart",
        "items" : [
            {
                "name":"chair",
                "price": 15.99,
                "item_id": 1
            }
        ],
        "store_id": 1
    }
]

users = [
    {
        "username":"spartan",
        "password": "pass1234"
    }
]

## UserCheck middleware
def make_secure(jina):
    def outer(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            for user in users:
                if user["username"] == jina:
                    if user["password"] == "pass1234":
                        return func(*args,**kwargs)
                raise PermissionError("You are not authorized!")
        return inner
    return outer

# Get Home
@app.get('/')
@make_secure("spartan")
def home():
    return "<h1>Country Road,Take me Hooome...</h1>"


# Get all stores
@app.get('/store') # http://localhost:5000/store
def get_stores():
    return {"stores": stores}

# Post New Store
@app.post('/store')
def create_store():
    global stores
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": [],
        "store_id": len(stores) + 1
    }
    stores.append(new_store)
    return new_store, 201

# Add new item to store
@app.post('/store/<string:name>/item')
def create_item(name):
    request_data = request.get_json()
    print(request_data)
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"],
                "item_id": len(store['items']) + 1
            }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found!"}, 404

#Get a single store
@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store, 200
    return {"message": f"Store {name} not found!"}, 404

#Get a single item from a store by ID
@app.get("/store/<string:name>/item/<int:item_id>")
def get_single_item(name,item_id):
    for store in stores:
        if store["name"] == name:
            for item in store["items"]:
                if item["item_id"] == item_id:
                    return item, 200
            return {"message": "No item found by that ID!"}, 404 
        return {"message": f"Store {name} not found!"}, 404


# Get items of a particular store
@app.get('/store/<string:name>/items')
def get_store_item(name):
    for store in stores:
        if store["name"] == name:
            return {"items":store["items"]}, 200  # ALWAYS TRY RETURNING DICTIONARIES
    return {"message": f"Store {name} not found!"}, 404
