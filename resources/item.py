import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import items, stores

from schemas import ItemSchema
from schemas import ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema) # put response decorator AFTER arguments
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            #this is an update dict sign (|=)
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # this handles a list of items
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # item_data is the processed JSON from ItemSchema
        for item in items.values():
            if(
                item_data["name"]==item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"{item} already exists")
        if item_data["store_id"] not in stores:
            abort(404, messaged="Store not found")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201