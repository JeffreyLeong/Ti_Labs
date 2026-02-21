from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app.expense_tracker.models import Category

class TransactionForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    type = SelectField(
        "Type",
        choices=[("income", "Income"), ("expense", "Expense"), ("transfer", "Transfer")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Transaction")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate category choices from DB
        self.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(active=True).all()]
