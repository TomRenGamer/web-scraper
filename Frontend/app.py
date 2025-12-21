"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug import Response

from Backend.App.Components.scrapeElement import *
from Backend.App.Components.csvWriter import *
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import IntegerField, StringField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import InputRequired, DataRequired, NumberRange, URL
import logging

""".
Initializing flask App with 'static_folder' and 'template_folder' property.
"""

flask = Flask(__name__,
              static_folder="./Styles",
              template_folder="./Templates")

"""
Configuration of csrf key for form protection.
"""

csrf = CSRFProtect(flask)
flask.config["SECRET_KEY"] = "secret123"

"""
Main class 'App' for initializing common functions for webscraper app.
"""


class App:
    def __init__(self) -> None:
        self.scraper = scrapeElement()
        self.logger = logging.getLogger(__name__)
        self.csv_writer = csvWriter()


"""
Class 'setOptionsForm' is representing an instance of WTForms subclass. Subclass represents form fields visible 
on website. It's used to set options like:
> amount of data to scrape
> specify website url

Fields:
> 'number_of_elements' is IntegerField which accepts integer values from 1 to 20. Default value is 1.
> 'page_url' represents StringField which accepts string value. It has special validation for websites url.
> 'submit' is SubmitField which is used to confirm data in previous fields.
"""


class setOptionsForm(FlaskForm):
    number_of_elements = IntegerField("Enter amount of elements to scrape:",
                                      validators=[DataRequired("Number of elements is required!"), NumberRange(min=1, max=20)],
                                      render_kw={"class": "numberOfElements"}, default=1)
    page_url = StringField("Enter website url:",
                           validators=[DataRequired("Website url is required!"), URL(message="Invalid website url!")],
                           render_kw={"class": "pageUrl", "required": False})
    submit = SubmitField("Submit")


"""
Class 'scrapeDataElement' is representing an instance of WTForms subclass. Subclass represents form fields visible 
on website used in FieldList for dynamic rendering fields based on elements to scrape amount. 
It's used to specify information's about container like:
> what container contains data,
> what does container have, class or id,
> what is the name of class or id.

Fields:
> 'header' represents StringField which accepts string value. It can't be empty.
> 'container' is SelectField from which You choose container that has the desired data.
> 'selectorType' represents SelectField that has 2 values - class or id. 
> 'selectorName' represents StringField which accepts string value. It can't be empty.
"""


class scrapeDataElement(FlaskForm):
    header = StringField("Enter header for element:",
                         validators=[DataRequired("Header is required!")],
                         render_kw={"class": "header", "required": False})
    container = SelectField("Choose container containing data:",
                            render_kw={"class": "container"},
                            choices=[("small", "small"), ("span", "span")])
    selectorType = SelectField("Does your container have class or id? (Choose 'class' or 'id'):",
                               render_kw={"class": "containerType"},
                               choices=[("class", "class"), ("id", "id")])
    selectorName = StringField("Enter name of class/id:",
                               validators=[DataRequired("Name of class/id is required!")],
                               render_kw={"class": "header", "required": False})


"""
Class 'scrapeDataForm' is representing an instance of WTForms subclass. Subclass represents form fields visible 
on website. It implements instance of 'scrapeDataElement' class for dynamic generating fields based on 
elements to scrape amount. It has SubmitField too.
"""


class scrapeDataForm(FlaskForm):
    elements = FieldList(FormField(scrapeDataElement), min_entries=1, max_entries=20)
    submit = SubmitField("Submit")


app = App()


@flask.route('/')
def home() -> str:
    return render_template("home.html")


@flask.route('/setOptions', methods=["POST", "GET"])
def set_options() -> Response | str:
    if request.method == "POST" or request.method == "GET":
        form = setOptionsForm()

        if form.validate_on_submit():
            number_of_elements = form.number_of_elements.data
            page_url = form.page_url.data

            return redirect(url_for("scrape_data", numberOfElements=number_of_elements, pageUrl=page_url))
        return render_template("setOptions.html", form=form)


@flask.route('/scrapeData', methods=["POST", "GET"])
def scrape_data() -> Response | str:
    if request.method == "POST" or request.method == "GET":
        form = scrapeDataForm()
        number_of_elements = request.args.get("numberOfElements", 1, type=int)
        page_url = request.args.get("pageUrl")

        while len(form.elements) < number_of_elements:
            form.elements.append_entry()

        if form.validate_on_submit():
            params = []
            raw_results = []
            results = []
            max_number_of_elements = 0
            headers = ["X"]

            for i, element_form in enumerate(form.elements):
                param = {
                    "header": element_form.header.data,
                    "container": element_form.container.data,
                    "selector_type": element_form.selectorType.data,
                    "selector_name": element_form.selectorName.data
                }

                params.append(param)

            for param in params:
                temp = [el for el in param.values()]
                headers.append(temp[0])
                raw_data = app.scraper.Scrape(page_url, temp[1], temp[2], temp[3])
                raw_results.append([x.text for x in raw_data])

            if raw_results:
                max_number_of_elements = max(len(r) for r in raw_results)
            else:
                max_number_of_elements = 0

            for i in range(max_number_of_elements):
                temp_el = [f"{i + 1}."]

                for j in range(len(raw_results)):
                    if i < len(raw_results[j]):
                        temp_el.append(raw_results[j][i])
                    else:
                        temp_el.append("")

                results.append(temp_el)

            session['scrape_results'] = {
                'results': results,
                'headers': headers,
                'numberOfElements': number_of_elements,
                'pageUrl': page_url,
                'headersAmount': len(headers)
            }

            return redirect(url_for("result"))

        return render_template("scrapeData.html", form=form, numberOfElements=number_of_elements, pageUrl=page_url)


@flask.route('/result', methods=["POST", "GET"])
def result() -> str:
    data = session.get('scrape_results', {})

    headers = data.get("headers")
    results = data.get("results", [])
    number_of_elements = data.get("numberOfElements", 0)
    page_url = data.get("pageUrl")

    return render_template("result.html", numberOfElements=number_of_elements, pageUrl=page_url,
                           results=results, headers=headers, headersAmount=len(headers))


if __name__ == "__main__":
    flask.run(port=4500)
