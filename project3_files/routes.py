from project3_files import app, mongo, forms
from wtforms import StringField, DateField, SelectField, DecimalField
from flask import request, render_template



# in the routes script we will create all of the calculated numbers that the user will see
# we will be doing all of the "business logic" that is envolved with presenting and maintaining an expenses app
@app.route('/')
def index():

    # ========== total expenses =============
    # the .db is the name of your database
    # .expenses is the collection within your db
    my_expenses = mongo.db.expenses.find()
    # this code will sum up the total expenses you've made in your collection
    total_expenses = 0
    for i in my_expenses:
        total_expenses += float(i["cost"])

    # ========== total category expenses =============
    # this will add up total cost per category in your collection
    # first, get a unique list of all our categories
    distinct_cat = mongo.db.expenses.distinct("category")
    # our function returns a dictionary object with the category totals
    category_expenses_dict = forms.get_category_expenses(distinct_cat)
    print("category_expenses_dict type:", type(category_expenses_dict))

    return render_template("index.html", total_expenses=total_expenses,category_expenses_dict=category_expenses_dict)


@app.route('/addExpenses', methods=["GET","POST"])
def addExpenses():
    # include form based off the Expenses class above
    if request.method == "POST":
        # insert the doc containing user data into database
        # it should be formatted as a dictionary
        return render_template("expenseAdded.html")

    render_template("addExpenses.html")#, form = expense_form)