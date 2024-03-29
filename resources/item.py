
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                            type=float, required=True,
                            help="This field cannot be left blank!"
                            )                    
    parser.add_argument("store_id",
                            type=int, required=True,
                            help="This field cannot be left blank!"
                            )                    
        

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404    

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": " An item with {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message":"an error occurred inserting the item."}, 500

        return item.json(), 200

    def delete (self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted."}

    def put(self, name):    
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name        
        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
       return {"item": [item.json() for item in ItemModel.query.all()]}
