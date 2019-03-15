from flask_restful import Resource, reqparse


class Hello(Resource):
    def get(self):
        return {'message': "Hello"}, 200


# 1. Resource operations that are more advanced than CRUD operations against a singleton should
#    have the singleton included in the name but then be more descriptive.  The example below is
#    StoreList which returns a list of Store.  These are
#    common when creating app specific calls that need to be more chunky to reduce round trips.
# 2. Explicitly include return status codes, even if the default status (my preference to be explicit).
# 3. Working against a single resource should have a singleton name.
class Store(Resource):
    # Unique identifier should not be included in the body data, it is received in the RI
    parser = reqparse.RequestParser()
    parser.add_argument('active',
                        type=bool,
                        required=False,
                        help="No help"
                        )
    parser.add_argument('lat',
                        type=float,
                        required=False,
                        help="No help"
                        )
    parser.add_argument('lng',
                        type=float,
                        required=False,
                        help="No help"
                        )

    # Delete all instances of the unique key, should only be one.
    # Always return success message even if key not found
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'store deleted'}, 200

    # Return first instance of unique key, there should only be one.
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': "store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    # PUT should receive all data to update.
    # PATCH accepts a subset of data to update.
    # This implementation will do a partial update in the PUT and not implement a PATCH.
    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name)

        if store:
            store.active = data['active']
        else:
            store = StoreModel(name, **data)

        store.save_to_db()

        return store.json(), 200


class StoreList(Resource):
    def get(self):
        # return {'stores': '[store.json() for store in StoreModel.query.all()]'}, 200
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200


from models.store_model import StoreModel
