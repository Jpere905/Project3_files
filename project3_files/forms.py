from project3_files import mongo
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired



# class for our forms
class Expenses(FlaskForm):
    # create the form for the following fields
    # StringField : description
    description = StringField("Description", validators=[DataRequired()])
    # SelectField : category
    distinct_cat = mongo.db.expenses.distinct("category")
    category = SelectField("Category",choices=distinct_cat, validators=[DataRequired()])
    # DecimalField : cost
    cost = DecimalField("Cost", validators=[DataRequired()])
    # DateField : date
    date = DateField("Date of purchase",
                     format='%m-%d-%Y',
                     validators=[DataRequired()],
                     render_kw={"placeholder": "mm-dd-yyyy"})

# when given a list of unique categories, this function will step through each item x and find every occurance of x in
# the collection and sum their values.
# returns a dictionary of { category : summed_price }
# distinct_cat is a list of unique categories
def get_category_expenses(distinct_cat):

    # will hold our {category : summed_price} pairs
    category_price_dict = {}

    for cat in distinct_cat:
        # print("cat var:", cat)
        # get only the documents with category <cat> and make an iterable object
        # also, only return the cost field
        unique_cat = mongo.db.expenses.find({"category": cat}, {"cost": 1})
        #print("unique_cat:", unique_cat)

        # zero out our total variable
        total = 0
        #print("item in unique_cat")
        for item in unique_cat:
            total += float(item["cost"])
            # print(item)

        #print("=====================================")
        #print("total of", cat, "is:", total)
        category_price_dict[cat] = total

    #print(category_price_dict.items())
    return category_price_dict


class TestForm(FlaskForm):
    name = StringField("Your name:")
    submit_name_form = SubmitField("Submit name")
