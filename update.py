from flask import jsonify
from config import time_format, entries
from bson.objectid import ObjectId

"""
Update functions
"""


# This function creates return information for AJAX when a field is updated.
def update_success_msg(field, timestamp, image=""):
    return jsonify({"status": "success",
                    "updated_on": timestamp.strftime(time_format),
                    "new_image": image,
                    "message": f"{field} sucessfully updated.",
                    "message_class": "valid-update"})


# This function sends information back to the frontend if a field cannot be updated
def update_failure_msg(message):
    return jsonify({"status": "failure",
                    "message": message,
                    "message_class": "invalid-update"})


# This function updates a document in the database with new information
def update_field(fields, entry_id):
    entries.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": fields}
        )