from backend import app
import db_access
import json
from bson import json_util

# Establish the database connection
db_access.db_connect()

with app.test_client() as client:
    # Test get_random_image
    random_image_response = client.get("/get_random_image")
    print("Get Random Image:", random_image_response.json)

    if random_image_response.status_code == 200:
        # Directly access the JSON data from the response
        image_data = random_image_response.json

        # Extract image ID from the random image response
        random_image_id = image_data['_id']['$oid']

        # Update the ELO rating of the random image
        update_elo_response = client.post("/update_image_elo", json={
            "imageIdOne": random_image_id,
            "newEloOne": 1200,
            "imageIdTwo": random_image_id,
            "newEloTwo": 1200
        })
        print("Update Image ELO:", update_elo_response.json)
    else:
        print("No random image found for ELO update test.")

    # Test top_elo_images
    top_elo_images_response = client.get("/top_elo_images")
    print("Top ELO Images:", top_elo_images_response.json)

    if top_elo_images_response.status_code == 200:
        print("Successfully retrieved top ELO images.")
    else:
        print(f"Failed to retrieve top ELO images. Status code: {top_elo_images_response.status_code}")
