from flask_restful import Api

from resources.store_resource import Hello, Store, StoreList

api = Api(prefix='')

api.add_resource(Hello, '/')  # Before init_app()
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
