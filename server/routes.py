from app import app, db
from flask import request, jsonify
from models import Thoughts

@app.route('/')
def hello():
    return "Hello"


# Route to Get all Thoughts
@app.route('/api/thoughts', methods=["GET"])
def get_thoughts():
    try:
        all_thoughts = Thoughts.query.all()  # Retrieve all Thought records from the database
        res = [thought.to_json() for thought in all_thoughts]  # Convert each Thought object to JSON-serializable format
        return jsonify(res), 200  # Return the response with HTTP 200 status code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to Create a Thought
@app.route('/api/thoughts', methods=["POST"])
def create_thought():
    try:
        data = request.json

        # Validations
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error": f'Missing required field: {field}'}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        # Fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"  # AVATAR API
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_thought = Thoughts(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_thought)
        db.session.commit()

        return jsonify(new_thought.to_json()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Route to Delete a Thought
@app.route("/api/thoughts/<int:id>", methods=["DELETE"])
def delete_thought(id):
    try:
        thought = Thoughts.query.get(id)
        if thought is None:
            return jsonify({"error": "Thought not found"}), 404

        db.session.delete(thought)
        db.session.commit()
        return jsonify({"msg": "Thought deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Route to Update a Thought
@app.route("/api/thoughts/<int:id>", methods=["PATCH"])
def update_thought(id):
    try:
        thought = Thoughts.query.get(id)
        if thought is None:
            return jsonify({"error": "Thought not found"}), 404

        data = request.json
        thought.name = data.get("name", thought.name)
        thought.role = data.get("role", thought.role)
        thought.description = data.get("description", thought.description)
        thought.gender = data.get("gender", thought.gender)

        db.session.commit()
        return jsonify(thought.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
  