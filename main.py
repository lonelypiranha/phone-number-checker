from flask import Flask, render_template, request, flash
from functions import validator, country_finder
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route("/", methods=["GET", "POST"])
def home(): 
    if request.method == "POST":
        form_data = request.form.to_dict()
        form_keys = form_data.keys()
        if ("validity" not in form_keys) and ("country" not in form_keys):
            telephone_number = form_data['tel-no']
            validity_status = False
            country_status = False
        elif "validity" not in form_keys:
            telephone_number = form_data['tel-no']
            validity_status = False
            country_status = True
        elif "country" not in form_keys:
            telephone_number = form_data['tel-no']
            validity_status = True
            country_status = False
        else:
            telephone_number = form_data['tel-no']
            validity_status = True
            country_status = True

        if not telephone_number:
            flash("Please input a telephone number")
        elif not re.match("^\+\d+$", telephone_number):
            flash("Please enter your phone number in the requested format")
        elif not(validity_status or country_status):
            flash("Please turn on at least one checker")
        else:
            if validity_status and country_status:
                validity_final = validator(telephone_number)
                country_final = country_finder(telephone_number)
                return render_template('index.html', validity_html = f"Validity: {validity_final}", country_html = f"Possible Countries: {country_final}")
            elif validity_status:
                validity_final = validator(telephone_number)
                return render_template('index.html', validity_html = f"Validity: {validity_final}")
            else:
                country_final = country_finder(telephone_number)
                return render_template('index.html', country_htmlx = f"Possible Countries: {country_final}")

    return render_template('index.html')
     
if __name__ == "__main__":
    app.run(debug=True)
    

