
from flask import Flask, render_template, request
from models import db, Product, Location
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///one.db' # change uri
app.config['SECRET_KEY'] = 'asdf' # import from someplace else

db.init_app(app)

@app.route('/')
def landing_page():
    return "landing page"

@app.route('/products')
def product_page():
	products = Product.query.all()
	for index, product in enumerate(products):
		temp_prod = {}
		temp_prod['id'] = product.id
		temp_prod['name'] = product.name
		products[index] = temp_prod
	return render_template('product.html', data={'products': products})

@app.route('/add_product', methods=["POST"])
def add_product():
	try:
		# print(request.get_json(force=True), "aasr")
		name = request.values["name"]
		new_prod = Product(name)
		db.session.add(new_prod)
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})

@app.route('/edit_product', methods=["POST"])
def edit_product():
	try:
		# print(request.get_json(force=True), "aasr")
		name = request.values["name"]
		prod_id = request.values["id"]
		prod = Product.query.filter_by(id=prod_id).first()
		prod.name = name
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})

@app.route('/locations')
def location_page():
	locations = Location.query.all()
	for index, location in enumerate(locations):
		temp_prod = {}
		temp_prod['id'] = location.id
		temp_prod['name'] = location.name
		locations[index] = temp_prod
	return render_template('location.html', data={'locations': locations})

@app.route('/add_location', methods=["POST"])
def add_location():
	try:
		# print(request.get_json(force=True), "aasr")
		name = request.values["name"]
		new_loc = Location(name)
		db.session.add(new_loc)
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})

@app.route('/edit_location', methods=["POST"])
def edit_location():
	try:
		# print(request.get_json(force=True), "aasr")
		name = request.values["name"]
		loc_id = request.values["id"]
		loc = Location.query.filter_by(id=loc_id).first()
		loc.name = name
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})


if __name__ == "__main__":
	app.run()

