from project3_files import app, mongo, forms
from wtforms import StringField, DateField, SelectField, DecimalField
from flask import request, render_template, redirect, url_for



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
    #print("category_expenses_dict type:", type(category_expenses_dict))

    return render_template("index.html", total_expenses=total_expenses,category_expenses_dict=category_expenses_dict)


# this route will be executed twice, the first time it will show the form page since the
# user has not submitted a POST request
# after submitting the form data, the route will run the second time, seeing that a POST request
# is made and enter the if statement below, which ultimately renders a new page
# maybe the number of return render_template() statements co-responds to the number of times a
# route will be executed?
@app.route('/addExpenses', methods=["GET","POST"])
def addExpenses():


    expense_form = forms.Expenses(request.form)
    # include form based off the Expenses class above
    if request.method == "POST":
        # insert the doc containing user data into database
        # it should be formatted as a dictionary
        # get our user provided data
        description = request.form["description"]
        category    = request.form["category"]
        cost        = request.form["cost"]
        date        = request.form["date"]

        # insert into our db
        mongo.db.expenses.insert({"description" : description,
                                    "category" : category,
                                    "cost" : cost,
                                    "date" : date})

        #return redirect(url_for("index"))

        return render_template("expenseAdded.html")

    return render_template("addExpenses.html", form = expense_form)