from flask import Flask, render_template, request, url_for, render_template
from wiki import horoscopebday, get_SP500
import random
from datetime import datetime

application = Flask(__name__)


def valid_date(date):
    try:
        d = datetime.strptime(date, '%d/%m')
    except ValueError:
        return False
    return d.day, d.month


@application.route("/", methods=["POST", "GET"])
def login():
    companies = []
    text = ""
    if request.method == "POST":
        user = request.form["nm"]
        date = valid_date(user)

        if not date:
            text = "Not a valid date!"
            return render_template("stock.html", companies=companies, wew=text)

        day, month = date
        lst_of_company, text = horoscopebday(day, month, get_SP500())
        companies = random.sample(lst_of_company, k=5)

    return render_template("stock.html", companies=companies, wew=text)


if __name__ == "__main__":
    application.run(debug=True)
