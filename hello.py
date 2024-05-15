from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# statyczna baza danych
stock = [
    {'item': 'RC_Car',
     'price': 100.00,
     'quantity': 10},
    {'item': 'RC_Plane',
     'price': 200.00,
     'quantity': 5},
    {'item': 'RC_Boat',
     'price': 150.00,
     'quantity': 7},
    {'item': 'RC_Helicopter',
     'price': 250.00,
     'quantity': 3}
]

# baza danych użytkowników
users = [
    {'user_id': '1', 'name': 'John Doe'},
    {'user_id': '2', 'name': 'Jane Smith'},
    {'user_id': '27056', 'name': 'Antoni Lichocki'}
]

# rezerwacje
reservations = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock/html')
def render_stock_html():
    return render_template('stock.html', stock=stock)


@app.route('/text_form', methods=['GET', 'POST'])
def text_form():
    if request.method == 'POST':
        received_text = request.form.get('text')
        received_text2 = request.form.get('text2')
        print("Received text:", received_text, received_text2)
        return "Received text: " + received_text + ' ' + received_text2
    return render_template(
        'text_form.html')


@app.route('/reservations/new', methods=['GET', 'POST'])
def new_reservation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        item_name = request.form['item_name']
        days = int(request.form['days'])
        start_date = request.form['start_date']

        item = next((i for i in stock if i["item"] == item_name), None)
        if item:
            total_cost = item["price"] * days
            reservation = {
                "user_id": user_id,
                "item_name": item_name,
                "days": days,
                "start_date": start_date,
                "total_cost": total_cost
            }
            reservations.append(reservation)
            print(reservations)
            return render_template('reservation_summary.html',
                                   reservation=reservation)
        else:
            return "Item not found", 404
    return render_template('new_reservation.html', users=users, stock=stock)


@app.route('/reservations', methods=['GET', 'POST'])
def view_reservations():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_reservations = [r for r in reservations if
                             r['user_id'] == user_id]
        user = next((u for u in users if u["user_id"] == user_id), None)
        user_name = user['name'] if user else 'Unknown User'
        return render_template('view_reservations.html', reservations=user_reservations,
                               user_name=user_name)
    return render_template('view_reservations_form.html')


# REST API routes for stock management

# To jest dekorator, który mówi, że funkcja poniżej ma być wywołana, gdy wejdziemy na stronę /stock i wyślemy żądanie
# GET.
@app.route('/stock', methods=['GET'])
def get_stock():
    return jsonify(stock)


# To jest dekorator, który mówi, że funkcja poniżej ma być wywołana, gdy wejdziemy na stronę /stock i wyślemy żądanie
# POST.
@app.route('/stock', methods=['POST'])
def add_item():
    stock.append(request.json)
    return jsonify(stock), 201


# To jest dekorator, który mówi, że funkcja poniżej ma być wywołana, gdy wejdziemy na stronę
# /stock/update_price/<item> i wyślemy żądanie PUT.
@app.route('/stock/update_price/<item>', methods=['PUT'])
def update_price(item):
    data = request.get_json()
    new_price = data.get('price')

    for product in stock:
        if product['item'] == item:
            product['price'] = new_price
            return jsonify(
                {"message": f"Price for {item} updated successfully to {new_price}"})

    return jsonify({"message": f"Item '{item}' not found"}), 404


# To jest dekorator, który mówi, że funkcja poniżej ma być wywołana, gdy wejdziemy na stronę
# /stock/delete_item/<item> i wyślemy żądanie DELETE.
@app.route('/stock/delete_item/<item>', methods=['DELETE'])
def delete_item(item):
    global stock
    stock = [product for product in stock if
             product['item'] != item]
    return jsonify({"message": f"Item '{item}' deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
