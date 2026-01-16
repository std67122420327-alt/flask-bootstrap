from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = b'your_secret_key_here'

cars = [
  {'id':1, 'brand': 'Toyata', 'model': 'Yaris Ative', 'year': 2024, 'price': 620000},
  {'id':2, 'brand': 'Toyata', 'model': 'Yaris Cross', 'year': 2025, 'price': 850000},
  {'id':3, 'brand': 'Mitsubishi', 'model': 'X-Force', 'year': 2025, 'price': 860000}
]

@app.route('/')
def index():
  return render_template('index.html',
                         title='Home Page')

@app.route('/cars')
def show_cars():
  search_query = request.args.get('q', '').lower()
  if search_query:
    filtered_cars = [car for car in cars if search_query in car['brand'].lower() or search_query in car['model'].lower()]
  else:
    filtered_cars = cars
  return render_template('car/cars.html',
                         title='Cars Page',
                         cars=filtered_cars)

@app.route('/search-cars')
def search_cars():
  search_query = request.args.get('q', '').lower()
  if search_query:
    filtered_cars = [car for car in cars if search_query in car['brand'].lower() or search_query in car['model'].lower()]
  else:
    filtered_cars = cars
  
  # Return only the table body HTML for HTMX
  return render_template_string('''
{% for car in cars %}
  <tr>
    <th scope="row">{{loop.index}}</th>
    <td>{{car.id}}</td>
    <td><a href="{{url_for('edit_car', id=car.id)}}" class="text-decoration-none">{{car.brand}}</a></td>
    <td><a href="{{url_for('edit_car', id=car.id)}}" class="text-decoration-none">{{car.model}}</a></td>
    <td>
      <a href="{{url_for('edit_car', id=car.id)}}" class="btn btn-outline-primary btn-sm me-2">
        <i class="bi bi-pencil-square"></i>
        Edit
      </a>
      <a href="{{url_for('delete_car', id=car.id)}}" class="btn btn-outline-danger btn-sm">
        <i class="bi bi-journal-x"></i>
        Delete
      </a>
    </td>
  </tr>
{% endfor %}
''', cars=filtered_cars)

@app.route('/cars/new', methods=['GET', 'POST'])
def new_car():
  if request.method == 'POST':      # กด submit
    brand = request.form['brand']
    model = request.form['model']
    year = int(request.form['year'])
    price = int(request.form['price'])

    length = len(cars)
    if length > 0:
      id = cars[length-1]['id'] + 1
    else:
      id = 1
    car = {'id':id, 'brand': brand, 'model': model, 'year': year, 'price': price}

    cars.append(car)
    flash('Add new car successfully', 'success')
    return redirect(url_for('show_cars'))


  return render_template('car/new_car.html',
                         title='New Car Page')

@app.route('/cars/<int:id>/delete')
def delete_car(id):
  for car in cars:
    if id == car['id']:
      cars.remove(car)
      flash('Delete car successfully', 'success')
      break

  return redirect(url_for('show_cars'))

@app.route('/cars/<int:id>/edit', methods=['GET', 'POST'])
def edit_car(id):
  car = None
  for c in cars:
    if c['id'] == id:
      car = c
      break
  
  if car is None:
    flash('Car not found', 'danger')
    return redirect(url_for('show_cars'))
  
  if request.method == 'POST':
    car['brand'] = request.form['brand']
    car['model'] = request.form['model']
    car['year'] = int(request.form['year'])
    car['price'] = int(request.form['price'])
    flash('Car updated successfully', 'success')
    return redirect(url_for('show_cars'))

  return render_template('car/edit_car.html',
                         title='Edit Car Page',
                         car=car)

if __name__ == '__main__':
    app.run(debug=True)

    @app.route('/cars/search')
    def search_cars():
        brand = request.args.get('brand')
        tmp_cars = []
        for car in cars:
         if brand in car ['brand']:
            tmp_cars.append(car)

            return render_template('car/search_cars.html',
                                   title='Search Car Page',
                                   cars=tmp_cars)
         