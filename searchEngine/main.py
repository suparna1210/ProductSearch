from flask import Flask
from flask_restful import Api, Resource
import es_management
from flask import render_template
from flask import request

app = Flask(__name__)
api = Api(app)

es_management = es_management.EsManagement()


@app.route("/")
def home():
    data_dict_array = es_management.getALlData()
    return render_template("index.html", sortOrder="asc", data_dict_list=data_dict_array)


@app.route("/search", methods=["POST"])
def search():
    name = request.form.get("name")
    brand = request.form.get("brand")
    categories = request.form.get("categories")
    sortOrder = request.form.get("sortOrder")
    form_dict = {}
    if name:
        form_dict["name"] = name

    if brand:
        form_dict["brand"] = brand

    if categories:
        form_dict["categories"] = categories

    data_dict_array = es_management.search(form_dict)
    print("No of records: %d" % len(data_dict_array))
    if sortOrder == "asc":
        sortOrder = "desc"
    else:
        sortOrder = "asc"
    return render_template("index.html", name=name, brand=brand, categories=categories, sortOrder=sortOrder, data_dict_list=data_dict_array)


@app.route("/osearch", methods=["POST"])
def searchOrderByPrice():
    name = request.form.get("h_name")
    brand = request.form.get("h_brand")
    categories = request.form.get("h_categories")
    sort_order = request.form.get("sortOrder")
    form_dict = {}
    if name:
        form_dict["name"] = name

    if brand:
        form_dict["brand"] = brand

    if categories:
        form_dict["categories"] = categories

    data_dict_array = es_management.searchWithSorting(form_dict, sort_order)
    print("No of records: %d" % len(data_dict_array))
    if sort_order == "asc":
        sort_order = "desc"
    else:
        sort_order = "asc"
    return render_template("index.html", name=name, brand=brand, categories=categories, sortOrder=sort_order, data_dict_list=data_dict_array)


@app.route("/populate", methods=["PUT"])
def populateDataToIndex():
    es_management.populate_index()
    return "Success", 201


if __name__ == "__main__":
    es_management.create_index()
    # es_management.populate_index()
    app.run(debug=True)
