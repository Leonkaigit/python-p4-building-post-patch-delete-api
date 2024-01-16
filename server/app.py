from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        description=data.get('description'),
        
    )

    db.session.add(new_baked_good)
    db.session.commit()

    baked_good_dict = new_baked_good.to_dict()

    response = make_response(
        jsonify(baked_good_dict),
        201
    )

    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery is None:
        response_body = {"message": "Bakery not found"}
        return make_response(jsonify(response_body), 404)

    data = request.form
    new_name = data.get('name')

    if new_name:
        bakery.name = new_name
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            jsonify(bakery_dict),
            200
        )

        return response
    else:
        response_body = {"message": "Name is required in the form"}
        return make_response(jsonify(response_body), 400)


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if baked_good is None:
        response_body = {"message": "Baked Good not found"}
        return make_response(jsonify(response_body), 404)

    db.session.delete(baked_good)
    db.session.commit()

    response_body = {
        "delete_successful": True,
        "message": "Baked Good deleted."
    }

    response = make_response(
        jsonify(response_body),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
