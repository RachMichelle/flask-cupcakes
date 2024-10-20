"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/api/cupcakes')
def get_list_cupcakes():

    cupcakes=Cupcake.query.all()
    serialized=[cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):

    cupcake=(Cupcake.query.get_or_404(cupcake_id)).serialize()
    
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():

    flavor=request.json['flavor']
    size=request.json['size']
    rating=request.json['rating']
    image=request.json.get('image', None)

    new_cupcake=Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):

    cupcake=Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor=(request.json.get('flavor', cupcake.flavor))
    cupcake.size=(request.json.get('size', cupcake.size))
    cupcake.rating=(request.json.get('rating', cupcake.rating))
    cupcake.image=(request.json.get('image', cupcake.image))

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):

    cupcake=Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")