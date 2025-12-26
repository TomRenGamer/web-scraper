from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired


class ScrapeDataElement(FlaskForm):
    """
    Form representing a single scraping configuration.

    Used as a nested form inside a FieldList to dynamically generate
    scraping definitions for multiple elements.
    """

    header = StringField(
        "Enter header for element:",
        validators=[DataRequired("Header is required!")],
        render_kw={"class": "header"}
    )

    container = SelectField(
        "Choose container containing data:",
        choices=[("small", "small"), ("span", "span")],
        render_kw={"class": "container"}
    )

    selector_type = SelectField(
        "Does your container have class or id?",
        choices=[("class", "class"), ("id", "id")],
        render_kw={"class": "selectorType"}
    )

    selector_name = StringField(
        "Enter name of class/id:",
        validators=[DataRequired("Name of class/id is required!")],
        render_kw={"class": "selectorName"}
    )


class ScrapeDataForm(FlaskForm):
    """
    Form for defining multiple scraping elements.

    Dynamically generates a list of ScrapeDataElement forms
    based on the number of elements specified by the user.
    """

    elements = FieldList(
        FormField(ScrapeDataElement),
        min_entries=1,
        max_entries=20
    )

    submit = SubmitField("Submit")
