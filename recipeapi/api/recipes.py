from flask import Flask, request, Response, jsonify
from recipeapi.storage.storage import Storage
from .status_responses import invalid_route, not_found, resource_exists, bad_request, resource_success
from schema import SchemaError
from .schemas import validate_schema, CreateRecipeSchema, EditRecipeSchema

app = Flask(__name__)
storage = Storage()

@app.route('/recipes/by/ingredient/<int:id_>', methods=['GET'])
def get_recipes_by_ingredient_id(id_:int) -> Response:
   recipe = storage.get_items('recipes', by_related='ingredients',attr_filters={'id':id_})
   if recipe is None:
      return not_found(request.path, id_)
   else:
      return jsonify(recipe)

@app.route('/recipes/<int:id_>', methods=['GET'])
def get_recipe_by_id(id_:int) -> Response:
   recipe = storage.get_item('recipes', attr_filters={'id':id_})
   if recipe is None:
      return not_found(request.path, id_)
   else:
      return jsonify(recipe)

@app.route('/recipes', methods=['GET'])
def get_recipes() -> Response:
   return jsonify(storage.get_items('recipes'))

@app.route('/recipes', methods=['POST'])
@validate_schema(CreateRecipeSchema)
def create_recipe() -> Response:
   collection = 'recipes'
   name = request.json['name']
   if storage.item_exists(collection, attr_filters={'name':name}):
      return resource_exists(request.path, name, additional_message="Please send a 'PUT' request to update the existing recipe.")
   else:
      storage.add_item(collection, name, data=request.json)
      return resource_success(collection, name, verb='added', code=201)

@app.route('/recipes/<int:id_>', methods=['PUT'])
@validate_schema(EditRecipeSchema)
def edit_recipe(id_:int) -> Response:
   collection = 'recipes'
   if not storage.item_exists(collection, attr_filters={'id':id_}):
      return not_found(request.path, id_)
   else:
      storage.update_item(collection, id_, data=request.json)
      return resource_success(collection, id_, verb='updated', code=200)

@app.route('/recipes/<int:id_>', methods=['DELETE'])
def delete_recipe(id_:int) -> Response:
   collection = 'recipes'
   if not storage.item_exists(collection, attr_filters={'id':id_}):
      return not_found(request.path, id_)
   else:
      storage.delete_item(collection, id_)
      return resource_success(collection, id_, verb='deleted', code=200)