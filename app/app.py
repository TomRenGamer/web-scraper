"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

Flask web application for configurable web scraping and CSV export.

The application allows the user to:
- specify a target website URL,
- choose the number of elements to scrape,
- define HTML containers and selectors dynamically using WTForms.
"""

from werkzeug import Response
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect

from components.scrapeElement import ScrapeElement
from components.csvWriter import CsvWriter

from forms.setOptionsForm import *
from forms.scrapeDataForm import *

import logging
import os
import secrets


flask = Flask(__name__,
              static_folder="./static",
              template_folder="./templates"
              )

flask.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(flask)


class App:
    """
    Application service container.

    Holds shared instances used across the application, such as:
    - the web scraper,
    - the CSV writer.
    """

    def __init__(self) -> None:
        self.scraper = ScrapeElement()
        self.csv_writer = CsvWriter()
        self.logger = logging


app = App()


@flask.route("/")
def home() -> str:
    """
    Render the home page.

    Returns:
        str: Rendered HTML template.
    """
    app.logger.info("Successfully rendered 'home.html' template")
    return render_template("home.html")


@flask.route("/setOptions", methods=["GET", "POST"])
def set_options() -> Response | str:
    """
    Handle scraping options form.

    Validates user input and redirects to the scraping configuration view.

    Returns:
        Response | str: Redirect response or rendered template.
    """
    form = SetOptionsForm()

    if form.validate_on_submit():
        number_of_elements = form.number_of_elements.data
        page_url = form.page_url.data

        app.logger.debug(f"Params from 'set_options()' -> number_of_elements: {number_of_elements}, "
                         f"page_url: {page_url}")

        app.logger.info("Redirecting to 'scrape_data' endpoint")
        return redirect(
            url_for(
                "scrape_data",
                numberOfElements=number_of_elements,
                pageUrl=page_url
            )
        )

    return render_template("setOptions.html", form=form)


@flask.route("/scrapeData", methods=["GET", "POST"])
def scrape_data() -> Response | str:
    """
    Handle scraping configuration and execute scraping logic.

    Dynamically builds scraping parameters, runs the scraper,
    and stores results in the session.

    Returns:
        Response | str: Redirect response or rendered template.
    """
    form = ScrapeDataForm()
    number_of_elements = request.args.get("numberOfElements", 1, type=int)
    page_url = request.args.get("pageUrl")

    while len(form.elements) < number_of_elements:
        form.elements.append_entry()

    if form.validate_on_submit():
        params = []
        raw_results = []
        results = []
        headers = ["X"]

        for element_form in form.elements:
            params.append({
                "header": element_form.header.data,
                "container": element_form.container.data,
                "selector_type": element_form.selector_type.data,
                "selector_name": element_form.selector_name.data,
                "elements_in_container": element_form.elements_in_container.data
            })

        for param in params:
            headers.append(param["header"])
            raw_data = app.scraper.scrape(
                page_url,
                param["container"],
                param["selector_type"],
                param["selector_name"],
                param["elements_in_container"]
            )
            raw_results.append([app.scraper.extract_text(el, param["elements_in_container"]) for el in raw_data])

        max_rows = max((len(r) for r in raw_results), default=0)

        for i in range(max_rows):
            row = [f"{i + 1}."]
            for column in raw_results:
                row.append(column[i] if i < len(column) else "")
            results.append(row)

        app.logger.debug(
            f"Params from 'scrape_data()' -> results: {results}, headers: {headers}, "
            f"numberOfElements: {number_of_elements}, pageUrl: {page_url}, headersAmount: {headers}, elementsInContainer: {element_form.elements_in_container.data}")

        session["scrape_results"] = {
            "results": results,
            "headers": headers,
            "numberOfElements": number_of_elements,
            "pageUrl": page_url,
            "headersAmount": len(headers),
            "elementsInContainer": element_form.elements_in_container.data
        }

        app.logger.info("Redirecting to 'result' endpoint")
        return redirect(url_for("result"))

    return render_template(
        "scrapeData.html",
        form=form,
        numberOfElements=number_of_elements,
        pageUrl=page_url
    )


@flask.route("/result", methods=["GET"])
def result() -> str:
    """
    Display scraping results.

    Reads scraping data from the session and renders the result view.

    Returns:
        str: Rendered HTML template with scraping results.
    """
    data = session.get("scrape_results", {})

    return render_template(
        "result.html",
        numberOfElements=data.get("numberOfElements", 0),
        pageUrl=data.get("pageUrl"),
        results=data.get("results", []),
        headers=data.get("headers", []),
        headersAmount=len(data.get("headers", []))
    )


if __name__ == "__main__":
    app.logger.info("Started app")
    flask.run(port=4500)
