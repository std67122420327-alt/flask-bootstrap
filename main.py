from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = b'hhijjohghdyuyujopi'

DATA_FILE = 'cars.json'

def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [
        {'id':1, 'brand': 'Toyota', 'model': 'Yaris Ative', 'year': 2024, 'price': 620000},
        {'id':2, 'brand': 'Toyota', 'model': 'Yaris Cross', 'year': 2025, 'price': 850000},
        {'id':3, 'brand': 'Mitsubishi', 'model': 'X-Force', 'year': 2025, 'price': 860000}
    ]

def save_cars():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(cars, f, indent=2, ensure_ascii=False)

cars = load_cars()

@app.route('/')
def index():
  return render_template('index.html',
                         title='Home Page')

@app.route('/cars')
def show_cars():
  return render_template('car/cars.html',
                         title='Cars Page',
                         cars=cars)

@app.route('/cars/new', methods=['GET', 'POST'])
def new_car():
  if request.method == 'POST':      # กด submit
    brand = request.form['brand']
    model = request.form['model']
    year = int(request.form['year'])
    price = int(request.form['price'])

    length = len(cars)
    if length>0:
      id = cars[length-1]['id'] + 1
    else:
      id = 1

    car = {'id':id, 'brand': brand, 'model': model, 'year': year, 'price': price}

    cars.append(car)
    save_cars()
    flash('Add new car successfully', 'success')

    return redirect(url_for('show_cars'))


  return render_template('car/new_car.html',
                         title='New Car Page')

@app.route('/cars/<int:id>/edit', methods=['GET', 'POST'])
def edit_car(id):
  for c in cars:
    if id == c['id']:
      car = c
      break

  if request.method == 'POST':      # กด submit
    brand = request.form['brand']
    model = request.form['model']
    year = int(request.form['year'])
    price = int(request.form['price'])
    # id = int(request.form['id'])

    for car in cars:
      if id == car['id']:
        car['brand'] = brand
        car['model'] = model
        car['year'] = year
        car['price'] = price
        save_cars()
        flash('Update car successfully', 'success')
        break

    return redirect(url_for('show_cars'))
  
  return render_template('car/edit_car.html',
                         title='Edit Car Page',
                         car=car)

@app.route('/cars/<int:id>/delete')
def delete_car(id):
  for car in cars:
    if id == car['id']:
      cars.remove(car)
      save_cars()
      flash('Delete car successfully', 'success')
      break
  
  return redirect(url_for('show_cars'))

@app.route('/cars/search')
def search_car():
  brand = request.args.get('brand')
  tmp_cars = []
  for car in cars:
    if brand in car['brand']:
      tmp_cars.append(car)
  
  return render_template('car/search_cars.html',
                         title='Search Car Page',
                         cars=tmp_cars)