from flask import Flask, render_template, request
from Backend.App.Components.scrapeElement import *

flask = Flask(__name__,
              static_folder="./Styles",
              template_folder="./Templates")


class App:
    def __init__(self) -> None:
        self.scraper = scrapeElement()


app = App()


@flask.route('/')
def home():
    return render_template("home.html")


@flask.route('/setOptions', methods=["POST", "GET"])
def set_options():
    if request.method == "POST" or request.method == "GET":
        number_of_elements = request.form.get("numberOfElements", 1)
        page_url = request.form.get("pageUrl", "")

        return render_template("setOptions.html", numberOfElements=int(number_of_elements), pageUrl=page_url)


@flask.route('/scrapeData', methods=["POST", "GET"])
def scrape_data():
    if request.method == "POST" or request.method == "GET":
        number_of_elements = request.form.get("numberOfElements", 1)
        page_url = request.form.get("pageUrl", "")

        return render_template("scrapeData.html", numberOfElements=int(number_of_elements), pageUrl=page_url)


@flask.route('/result', methods=["POST", "GET"])
def result():
    if request.method == "POST" or request.method == "GET":
        params = []
        raw_results = []
        results = []
        max_number_of_elements = 0
        headers = ["X"]
        number_of_elements = request.form.get("numberOfElements")
        page_url = request.form.get("pageUrl")

        for i in range(0, int(number_of_elements)):
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

        return render_template("result.html", numberOfElements=int(number_of_elements), pageUrl=page_url,
                               results=results, headers=headers, headersAmount=len(headers))


if __name__ == "__main__":
    flask.run(port=4500)
