from flask import Flask, render_template, request, redirect, url_for,flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine,desc,func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/')
def restaurant():
	res = session.query(Restaurant).all()
	return render_template('resMenu.html',restaurant=res)


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def restaurantEdit(restaurant_id):
	res = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		res.name = request.form['name']
		session.add(res)
		session.commit()
		flash("Restaurant renamed!")
		return redirect(url_for('restaurant'))
	else:	
		return render_template('editRes.html',restaurant=res)

@app.route('/restaurant/new/', methods=['GET','POST'])
def restaurantNew():
	if request.method == 'POST':
		newRes = Restaurant(name = request.form['name'])
		session.add(newRes)
		session.commit()
		flash("New Restaurant Created!")
		return redirect(url_for('restaurant'))
	else:
		return render_template('newRes.html')

@app.route('/restaurant/<int:restaurant_id>/delete/',methods=['GET','POST'])
def restaurantDelete(restaurant_id):
	res = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		items = session.query(MenuItem).filter_by(restaurant_id = res.id).delete()	
		session.delete(res)
		session.commit()
		flash("A Restaurant Deleted!")
		return redirect(url_for('restaurant'))
	else:
		return render_template('delRes.html',restaurant=res)

@app.route('/restaurant/<int:restaurant_id>/',)
def restaurantMenu(restaurant_id):
	res = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=res.id)
	count = items.count()
	if count == 0:
		count = True
	else:
		count = False
	print count
	return render_template('templates.html',restaurant=res,items=items,count=count)
	
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],price=request.form['price'],description=request.form['disc'],restaurant_id= restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New Menu Item Created!")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
    		return render_template('newMenuItem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	Item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		flash(Item.name +" Menu Changed to "+ request.form['name'])
		if (request.form['name']):
			Item.name = request.form['name']
		if (request.form['price']):
			Item.price = request.form['price']
		if (request.form['disc']):
			Item.description = request.form['disc']
		session.add(Item)
		session.commit()
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
    		return render_template('editMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,Item=Item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	Item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		flash(Item.name +" Menu Item Deleted")
		session.delete(Item)
		session.commit()
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
    		return render_template('deleteMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,Item=Item)

@app.route('/restaurant/JSON')
def restaurantJSON():
	res = session.query(Restaurant).all()
	return jsonify(Restaurant=[i.serialize for i in res])
    
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	res = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items =session.query(MenuItem).filter_by(restaurant_id=res.id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	res = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items =session.query(MenuItem).filter_by(restaurant_id=res.id).filter_by(id=menu_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])   
	
	 
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
