from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, URL


# def is_scraping_allowed() -> None:
#     if


class SetOptionsForm(FlaskForm):
    """
    Form for setting basic scraping options.

    Allows the user to define:
    - the number of elements to scrape,
    - the target website URL.
    """

    number_of_elements = IntegerField(
        "Enter amount of elements to scrape:",
        validators=[
            DataRequired("Number of elements is required!"),
            NumberRange(min=1, max=20)
        ],
        render_kw={"class": "numberOfElements"},
        default=1
    )

    page_url = StringField(
        "Enter website url:",
        validators=[
            DataRequired("Website url is required!"),
            URL(message="Invalid website url!")
        ],
        render_kw={"class": "pageUrl"}
    )

    submit = SubmitField("Submit")
