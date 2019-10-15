
from flask import Flask, render_template, request
from models import db, Product, Location, ProductMovement
from sqlalchemy import or_, and_
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

@app.route('/movements')
def movement_page():
	movements = ProductMovement.query.all()
	for index, movement in enumerate(movements):
		# print(movement.from_location, movement.to_location, Location.query.all())
		temp_mov = {}
		temp_mov['id'] = movement.movement_id
		temp_mov["from"] = None
		temp_mov["to"] = None
		temp_mov["from_id"] = movement.from_location
		temp_mov["to_id"] = movement.to_location

		if movement.from_location:
			temp_mov['from'] = Location.query.filter_by(id=movement.from_location).first().name
		if movement.to_location:
			temp_mov['to'] = Location.query.filter_by(id=movement.to_location).first().name
		temp_mov["qty"] = movement.qty
		temp_mov["time"] = movement.timestamp
		temp_mov["prod_id"] = movement.product_id
		temp_mov["prod"] = Product.query.filter_by(id=movement.product_id).first().name
		movements[index] = temp_mov

	
	# calculation of final stuff
	locations = Location.query.all()
	location_totals = {}
	for location in locations:
		movs_in_loc = ProductMovement.query.filter(or_(ProductMovement.from_location == location.id, 
														  ProductMovement.to_location == location.id)).all()
		# listing all products involved in this location
		products_in_loc = []
		for mov in movs_in_loc:
			if mov.product_id not in products_in_loc:
				products_in_loc.append({
										'id': mov.product_id,
										'name': Product.query.filter_by(id=mov.product_id).first().name
										})
		loc_prod_count = {}
		print(products_in_loc)
		for product in products_in_loc:
			# calculating amount of products remaining or due from this location
			movs_plus = ProductMovement.query.filter(and_(ProductMovement.to_location==location.id, ProductMovement.product_id==product['id'])).all()
			movs_minus = ProductMovement.query.filter(and_(ProductMovement.from_location==location.id, ProductMovement.product_id==product['id'])).all()
			count = 0
			for mov in movs_plus:
				count += mov.qty
			for mov in movs_minus:
				count -= mov.qty
			loc_prod_count[product['id']] = {'name':product['name'], 'count':count}
		location_totals[location.id] = {'name':location.name, 'counts':loc_prod_count}


	return render_template('movement.html', data={'movements': movements, 'location_totals': location_totals})

@app.route('/add_movement', methods=["POST"])
def add_movement():
	try:
		_from = request.values["from"]
		to = request.values["to"]
		p_id = request.values["prod"]
		qty = request.values["qty"]
		print(_from, to)
		movement = ProductMovement(int(p_id), _from, to, qty=qty)
		db.session.add(movement)
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})	

@app.route('/edit_movement', methods=["POST"])
def edit_movement():
	try:
		_id = request.values["id"]
		_from = request.values["from"]
		to = request.values["to"]
		p_id = request.values["prod"]
		qty = request.values["qty"]
		movement = ProductMovement.query.filter_by(movement_id=_id).first()
		movement.from_location = _from
		movement.to_location = to
		movement.product_id = p_id
		movement.qty = qty
		db.session.commit()
		return json.dumps({"success": True})
	except Exception as e:
		print(e)
		db.session.rollback()
		return json.dumps({"success": False})



if __name__ == "__main__":
	app.run()

