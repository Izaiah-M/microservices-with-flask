from ..config import mongo


# How you would typically create a model using mongo
class Books(mongo.db.create_collection):
    pass
