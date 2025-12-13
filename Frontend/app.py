from flask import Flask, render_template, request, redirect, url_for
from Backend.App.Components.scrapeElement import *
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, NumberRange, URL

flask = Flask(__name__,
              static_folder="./Styles",
              template_folder="./Templates")

flask.config["SECRET_KEY"] = "secret"


class App:
    def __init__(self) -> None:
        self.scraper = scrapeElement()


class setOptionsForm(FlaskForm):
    number_of_elements = IntegerField("Enter amount of elements to scrape:",
                                      validators=[InputRequired(), NumberRange(min=1, max=20)],
                                      render_kw={"class": "numberOfElements"}, default=1)
    page_url = StringField("Enter website url:",
                           validators=[InputRequired("Website url is required!"), URL(message="Invalid website url!")],
                           render_kw={"class": "pageUrl"})
    submit = SubmitField("Submit")


class scrapeDataForm(FlaskForm):
    header = StringField("Enter header for element:",
                         validators=[DataRequired("Header is required!")],
                         render_kw={"class": "header"})
    container = SelectField("Choose container containing data:",
                            render_kw={"class": "container"},
                            choices=[("small", "small"), ("span", "span")])
    selectorType = SelectField("Does your container have class or id? (Choose 'class' or 'id'):",
                               render_kw={"class": "containerType"},
                               choices=[("class", "class"), ("id", "id")])
    selectorName = StringField("Enter name of class/id:",
                               validators=[DataRequired("Name of class/id is required!")],
                               render_kw={"class": "header"})
    submit = SubmitField("Submit")


app = App()


@flask.route('/test_setOptions', methods=["POST", "GET"])
def form_setOptions():
    form = setOptionsForm()

    if form.validate_on_submit():
        number_of_elements = form.number_of_elements.data
        page_url = form.page_url.data

        return redirect(url_for("form_scrapeData", numberOfElements=number_of_elements, pageUrl=page_url))
    return render_template("test.html", form=form)


@flask.route('/test_scrapeData', methods=["POST", "GET"])
def form_scrapeData():
    form = scrapeDataForm()
    number_of_elements = request.args.get("numberOfElements", 1, type=int)
    page_url = request.args.get("pageUrl")

    if form.validate_on_submit():
        headers = form.header.data
        return f"<h1>{headers}</h1>"

    return render_template("test2.html", form=form, numberOfElements=number_of_elements, pageUrl=page_url)


@flask.route('/')
def home():
    return render_template("home.html")


@flask.route('/setOptions', methods=["POST", "GET"])
def set_options():
    if request.method == "POST" or request.method == "GET":
        number_of_elements = request.form.get("numberOfElements", 1, type=int)
        page_url = request.form.get("pageUrl", "")

        return render_template("setOptions.html", numberOfElements=number_of_elements, pageUrl=page_url)


@flask.route('/scrapeData', methods=["POST", "GET"])
def scrape_data():
    if request.method == "POST" or request.method == "GET":
        number_of_elements = request.form.get("numberOfElements", 1, type=int)
        page_url = request.form.get("pageUrl")

        return render_template("scrapeData.html", numberOfElements=number_of_elements, pageUrl=page_url)


@flask.route('/result', methods=["POST", "GET"])
def result():
    if request.method == "POST" or request.method == "GET":
        params = []
        raw_results = []
        results = []
        max_number_of_elements = 0
        headers = ["X"]
        number_of_elements = request.form.get("numberOfElements", type=int)
        page_url = request.form.get("pageUrl")

        for i in range(0, number_of_elements):
            params.append({
                "header": request.form.get("header" + f"{i}"),
                "container": request.form.get("container" + f"{i}"),
                "selector_type": request.form.get("selectorType" + f"{i}"),
                "selector_name": request.form.get("selectorName" + f"{i}")
            })

        for param in params:
            temp = [el for el in param.values()]
            headers.append(temp[0])
            raw_data = app.scraper.Scrape(page_url, temp[1], temp[2], temp[3])
            raw_results.append([x.text for x in raw_data])

        for i in range(1, len(raw_results)):
            if len(raw_results[i - 1]) > len(raw_results[i]):
                max_number_of_elements = len(raw_results[i - 1])
            else:
                max_number_of_elements = len(raw_results[i])

        for i in range(0, max_number_of_elements):
            temp_el = [f"{i + 1}."]

            for j in range(0, len(raw_results)):
                temp_el.append(raw_results[j][i])

            results.append(temp_el)

        return render_template("result.html", numberOfElements=number_of_elements, pageUrl=page_url,
                               results=results, headers=headers, headersAmount=len(headers))


if __name__ == "__main__":
    flask.run(port=4500)
