from app import app, db
from flask import request, jsonify
from models import Thoughts

@app.route('/')
def hello():
    return "Hello"


# Route to Get all Thoughts
@app.route('/thoughts', methods=["GET"])
def get_thoughts():
   
    all_thoughts = Thoughts.query.all()  # Retrieve all Thought records from the database

    res = [] 
    for thought in all_thoughts:
        res.append(thought.to_json())  # Convert each Thought object to a JSON-serializable format

    return jsonify(res)
@app.route('/thought',methods=["POST"])

def create_thoughts():
  try:
    data = request.json

    # Validations
    required_fields = ["name","role","description","gender"]
    for field in required_fields:
      if field not in data or not data.get(field):
        return jsonify({"error":f'Missing required field: {field}'}), 400

    name = data.get("name")
    role = data.get("role")
    description = data.get("description")
    gender = data.get("gender")

    # Fetch avatar image based on gender
    if gender == "male":
      img_url = f"https://avatar.iran.liara.run/public/boy?username={name}" #AVATAR  API:
    elif gender == "female":
      img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
    else:
      img_url = None

    new_Thoughts = Thoughts(name=name, role=role, description=description, gender= gender, img_url=img_url)

    db.session.add(new_Thoughts) 
    db.session.commit()

    return jsonify(new_Thoughts.to_json()), 201
    
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}), 500


# Delete a Thoughts
@app.route("/thought/<int:id>",methods=["DELETE"])
def delete_Thoughts(id):
  try:
    Thoughts = Thoughts.query.get(id)
    if Thoughts is None:
      return jsonify({"error":"Thoughts not found"}), 404
    
    db.session.delete(Thoughts)
    db.session.commit()
    return jsonify({"msg":"Thoughts deleted"}), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),500


# Update a Thoughts profile
@app.route("/thoughts/<int:id>",methods=["PATCH"])
def update_Thoughts(id):
  try:
    Thoughts = Thoughts.query.get(id)
    if Thoughts is None:
      return jsonify({"error":"Thoughts not found"}), 404
    
    data = request.json

    Thoughts.name = data.get("name",Thoughts.name)
    Thoughts.role = data.get("role",Thoughts.role)
    Thoughts.description = data.get("description",Thoughts.description)
    Thoughts.gender = data.get("gender",Thoughts.gender)

    db.session.commit()
    return jsonify(Thoughts.to_json()),200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),500