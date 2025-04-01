from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Funkce pro získání aktuálních kurzů z ČNB
def get_exchange_rates():
    url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"
    response = requests.get(url)
    lines = response.text.split("\n")[2:]  # Přeskakujeme hlavičku
    rates = {}

    for line in lines:
        parts = line.split("|")
        if len(parts) > 3:
            currency = parts[3]  # Kód měny (např. EUR, USD)
            rate = float(parts[4].replace(",", "."))  # Převod kurzu na float
            rates[currency] = rate
    return rates

# Endpoint pro získání kurzů
@app.route("/kurzy", methods=["GET"])
def kurzy():
    return jsonify(get_exchange_rates())

# Endpoint pro převod měn
@app.route("/convert", methods=["GET"])
def convert():
    amount = float(request.args.get("amount", 1))
    from_currency = request.args.get("from", "EUR")
    to_currency = request.args.get("to", "CZK")

    rates = get_exchange_rates()

    if from_currency == "CZK":
        result = amount / rates[to_currency]
    elif to_currency == "CZK":
        result = amount * rates[from_currency]
    else:
        result = amount * rates[from_currency] / rates[to_currency]

    return jsonify({"amount": amount, "from": from_currency, "to": to_currency, "result": result})

if __name__ == "__main__":
    app.run(debug=True)