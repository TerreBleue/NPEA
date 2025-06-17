from pymongo import MongoClient

# Database
client = MongoClient("mongodb://localhost:27017/")
db = client["NoiseData"]
collection = db["noise_data"]

def insert_noise_data(data):
    try:
        collection.insert_one(data)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")