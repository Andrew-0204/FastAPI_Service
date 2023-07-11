import motor.motor_asyncio
from pymongo import DESCENDING
import logging
from bson.objectid import ObjectId
from dotenv import dotenv_values

config = dotenv_values(".env")


class MongoAPI:
    def __init__(self, data):
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://uwb:uwb@uwb-api.i9ksnts.mongodb.net/")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    @staticmethod
    def value_helper(data) -> dict:
        result = {
            "id": str(data["_id"]),
        }
        if "number" in data:
            result["number"] = data["number"]
        if "args" in data:
            result["args"] = data["args"]
        return result

    async def all(self):
        values = []
        async for value in self.collection.find():
            values.append(self.value_helper(value))
        return values

    async def create(self, data):
        try:
            logging.info('Writing Data')
            new_document = data['Document']
            response = await self.collection.insert_one(new_document)
            output = {'Status': 'Successfully Inserted',
                      'Document_ID': str(response.inserted_id)}
            return output
        except Exception as e:
            logging.error(f"Error occurred while writing data: {e}")
            return {'Status': 'Error', 'Message': str(e)}

    async def write_result(self, data, res):
        try:
            logging.info('Writing Data')
            response = await self.collection.insert_one(res)
            output = {'Status': 'Successfully Inserted',
                      'Document_ID': str(response.inserted_id)}
            return output
        except Exception as e:
            logging.error(f"Error occurred while writing result: {e}")
            return {'Status': 'Error', 'Message': str(e)}

    async def update(self):
        try:
            filt = self.data['Filter']
            updated_data = {"$set": self.data['DataToBeUpdated']}
            response = await self.collection.update_one(filt, updated_data)
            output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
            return output
        except Exception as e:
            logging.error(f"Error occurred while updating data: {e}")
            return {'Status': 'Error', 'Message': str(e)}

    async def delete(self, data):
        try:
            filt = data['Document']
            response = await self.collection.delete_one(filt)
            output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
            return output
        except Exception as e:
            logging.error(f"Error occurred while deleting data: {e}")
            return {'Status': 'Error', 'Message': str(e)}

    async def get_last_document(self):
        try:
            logging.info('Finding Last Document')
            document = await self.collection.find_one({}, sort=[('_id', DESCENDING)])
            if document:
                output = {item: document[item] for item in document if item != '_id'}
                return output
            else:
                return None
        except Exception as e:
            logging.error(f"Error occurred while finding last document: {e}")
            return None

    # Retrieve a value with a matching ID
    async def retrieve_one_value(self, id: str) -> dict:
        student = await self.collection.find_one({"_id": ObjectId(id)})
        if student:
            return self.value_helper(student)
