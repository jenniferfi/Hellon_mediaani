from flask import Flask, json, jsonify, redirect, render_template, request
import statistics

# Configure application
app = Flask(__name__)

numbers = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Get user input one number at a time
        number = request.form.get("number")

        # Ensure user input was submitted
        if not number:
            return redirect("/")

        # Check that input is a number
        try:
            float(request.form.get("number"))
        except:
            print("Input is not a number")
            return redirect("/")

        # Add user input to list of numbers
        numbers.append(float(number))

        return redirect("/")

    else:

        # Ensure that there is at least 10 items in numbers list
        if len(numbers) > 9:
            # Calculate median
            median = statistics.median(numbers)
        else:
            median = "Please add at least 10 numbers"

        return render_template("index.html", numbers=numbers, median=median)


@app.route("/list", methods=["GET", "POST"])
def numbers_list():
    if request.method == "POST":
        
        # Get user input as a list
        numbers = request.form.get("list")

        # Ensure user input was submitted
        if not numbers:
            return redirect("/")
        else:
            numbers_list = json.loads(numbers)

        # todo: Check for only numbers in list

        # Ensure that there is at least 10 items in numbers list
        if len(numbers_list) > 9:
            # Calculate median
            median = statistics.median(numbers_list)
        else:
            median = "Please add at least 10 numbers"

        return render_template("index.html", numbers=numbers_list, median=median)

    else:
        return redirect("/")


@app.route('/api/median', methods=['POST'])
def calculate_median():

    # Get numbers as JSON
    numbers = request.json["numbers"]

    # Ensure that numbers is a list of at least 10 items
    if (isinstance(numbers, list) and len(numbers) >= 10):
        
        # Calculate and return median
        return jsonify(statistics.median(numbers))
    else:
        return "Bad request", 400


if __name__ == "__main__":
    app.run()