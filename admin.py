from flask import render_template, session, request, redirect, flash
from app import *
from model import *
from werkzeug.utils import secure_filename    #function from werkzeug to handle file uploads securely
import seaborn as sns
import matplotlib.pyplot as plt


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#allowed_file function to check if the given filename has an allowed extension
def allowed_file(filename):
    #'.' in filename: checks if there is a dot in the filename. It is used to separate filename from its extension
    #filename.rsplit('.', 1): splits filename into 2 parts (filename & extension) & splits the string at rightmost occurreence of dot
    #filename.rsplit('.', 1)[1]: selects 2nd part of split, i.e., file extension
    #filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS: checks if lowercase file extension is presentt in ALLOWED EXTENSIONS
    #True if file has allowed extension, otherwise, True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#ROUTE FOR ADMIN CONTROL MANAGEMENT SYSTEM
@app.route("/cms")
def admin_index():
    #Checks if "admon_id" key exists in the session
    if "admin_id" in session: 
        details_of_products=Product.query.all()
        # Sample data
        products = [detail.name for detail in details_of_products]
        qty = [detail.qty for detail in details_of_products]
        #Create a bar plot using Seaborn
        sns.set(style="whitegrid")  # Set the style of the plot
        plt.figure(figsize=(15, 15))  # Adjust the size of the plot
        #Create the bar plot
        ax = sns.barplot(x=products, y=qty, palette="viridis")
        # Rotate x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        #Adding labels and title
        plt.xlabel("Products", fontweight="bold")
        plt.ylabel("Quantity", fontweight="bold")
        plt.title("Inventory in Stock", fontweight="bold")
        #Save the plot as an image in static
        plt.savefig("static/output.png")
        #If admin is logged in
        return render_template("admin_index.html", flag=True)
    else:
        #If "admin_id" key not exists in the session
        #redirect admin to admin sign-in page to authenticate
        return redirect("/admin_sign-in")


#ROUTE FOR ADMIN SIGN-IN
@app.route("/admin_sign-in")
def admin_sign_in(): 
    #Checks if "admin_id" key exists in the session
    if "admin_id" in session:
        #If adminid already logged in, retrieve admin_id from session
        adminid = session["admin_id"]
        #Redirect to admin cms page
        return redirect ("/cms")
    #If "admin_id" not exists in session, render admin_sign-in template before accessing admin cms
    return render_template("admin_sign-in.html", flag=True)


#ROUTE FOR ADMIN SIGN-UP
@app.route("/admin_sign-up")
def admin_sign_up():
    return render_template("admin_sign-up.html", flag=True)


#ROUTE FOR HANDLING ADMIN LOGIN AUTHENTICATION
@app.route("/admin_login_authentication", methods=["POST"])             #
def admin_login():
    #If request method is POST
    if(request.method=="POST"):
        #Get the values submitted in the login form for email & password
        cemail = request.form.get("email")
        cpassword = request.form.get("password")
        #Query the admin table in the database for an admin with the provided email & password
        admin = Admin.query.filter_by(email=cemail, password=cpassword)
        #Convert the query result to a list
        check = [i for i in admin]
        if check:
            #If an admin with the provided credentials exusts, store their "id" in the session
            session["admin_id"] = check[0].id
            #Print admin_id for debugging purpose
            print(session["admin_id"])
            print("authentication done")
            #Redirect authenticated admin to admin cms
            return redirect("/cms")
        else:
            #If no admin with provided credentials is found, 
            print("not found")
            flash("INVALID EMAIL OR PASSWORD")
            #Redirect back to admin sign-in page
            return redirect("/admin_sign-in")
    else:
        #If request method is GET or other HTTP method
        return "bad request"
    

#ROUTE FOR HANDLING ADMIN LOGOUT    
#Route accepts only POST requests, ensuring that lohout is done securely using POST request. 
#Its good to prevent accidental logouts caused by unintended GET requests
@app.route("/admin_logout", methods=["POST"])
def admin_logout():
    #Check if "admin_id" key exists in session
    if("admin_id") in session:
        #Check if request method is POST
        if(request.method=="POST"):
            #Remove "admin_id" key from session to logout the admin
            session.pop("admin_id")
            print("logout")
            #Redirect the user back to admin sign-in page after successful logout
            return redirect("admin_sign-in")
        else:
            #If request method is GET or other HTTP method
            return "Bad request...Please give only POST request instead of {}".format(request.method) 
    else:
        #If "admin_id" not exists in the session
        #redirect the user back to admin sign-in page since there is no admin to log out
        return redirect("/admin_sign-in")


#ROUTE FOR HANDLING ADMIN REGISTRATION
@app.route('/admin_register', methods=["POST"])
def admin_register():
    if(request.method == "POST"):
        try:
            #Get the values submitted in the registration form
            cname = request.form.get("name")
            ccontact = request.form.get("contact_no")
            cemail = request.form.get("email")
            cpassword = request.form.get("password")
            csex = request.form.getlist("sex")
            #Create a new Admin with the provided information and the first sex value from the form
            for i in csex[:1]:
                update_admin_db = Admin(name=cname, contact_no=ccontact, email=cemail, password=cpassword, sex=i)
            #Add the new Admin to the database session
            db.session.add(update_admin_db)
            #Flush the session (for possible rollback)
            db.session.flush()
        except Exception as e:
            #If there is an exception during the registration process
            print("rollback")
            #Rollback the session 
            db.session.rollback()
            #Return an error message
            return "{}".format(e),"Not Registered"
        else:
            #If the registration process is successful, commit the changes in the database
            db.session.commit()
            #Query the Admin table in the database to find the newly registered admin by their email and password
            admin = Admin.query.filter_by(email=cemail, password=cpassword)
            check = [i for i in admin]
            if check:
                #If the newly registered admin is found, store their 'id' in the session
                session["admin_id"] = check[0].id
                #Redirect the newly registered admin to the admin cms
                return redirect("/cms")


#ROUTE FOR ADMIN CATEGORY CMS
@app.route("/admin_category_cms")
def admin_category_cms():
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Query all categories from Category table in the database
        category = Category.query.all()
        #Convert the query result to a list
        check = [i for i in category]
        #Render admin_category_cms template with the 'all_categories' variable containing the categories
        return render_template("admin_category_cms.html", all_categories = check, flag=True)
    else:
        #If "admin_id" key not exists in session
        #redirect the user back to admin sign-in page to handle authentication before accessing category cms
        return redirect("/admin_sign-in")
    

#ROUTE FOR ADMIN PRODUCT CMS (SPECIFIED)
@app.route("/admin_product_cms/<int:i>")
def admin_product_cms(i):
    #Check if "admin_id" key exists in the session
    if "admin_id" in session:
        #Query all products from Product table in the database that belongs to specified category
        product = Product.query.filter_by(category=i)
        #Convert the query result to a list
        check = [i for i in product]
        #Render admin_product_cms template with the 'all_products' variable containing the products
        return render_template("admin_product_cms.html", all_products = check, flag=True)
    else:
        #If "admin_id" key not exists in session
        #redirect the user back to admin sign-in page to handle authentication before accessing product cms
        return redirect("/admin_sign-in")
    

#ROUTE FOR ADMIN PRODUCT CMS (ALL)
@app.route("/admin_product_cms")
def admin_product_cms_all():
    #Check if "admin_id" key exists in the session
    if "admin_id" in session:
        #Query all products from Product table in the database
        product = Product.query.all()
        #Convert the query result to a list
        check = [i for i in product]
        #Render admin_product_cms template with the 'all_products' variable containing all products
        return render_template("admin_product_cms.html", all_products = check, flag=True)
    else:
        #If "admin_id" key not exists in session
        #redirect the user back to admin sign-in page to handle authentication before accessing product cms
        return redirect("/admin_sign-in")


#ROUTE FOR ADDING NEW CATEGORY IN ADMIN CATEGORY CMS
@app.route("/admin_category_add", methods=["GET", "POST"])
def admin_category_add():
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #If request method is POST, process the form submission to add a new category
        if request.method=="POST":
            #Get the category name and password from the form submitted by the admin
            category_name=request.form['category_name']
            password=request.form['password']
            #Get the uploaded file of image from the form submitted by the admin
            file = request.files['file']
            filename = None
            #Check if uploaded image file has allowed extension
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Query the Admin table in the database with the admin session ID and password
            #To verify the admin identity
            verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
            admin_check = [i for i in verify_admin]
            if admin_check:
                #If admin is verified and the file is successfully uploaded 
                if filename is not None:
                    #set image path in image 
                    image = "/static/"+filename
            #Create a new Category with the provided category name and image path
            new_category=Category(name=category_name, image=image)
            #Add the new Category to database session 
            db.session.add(new_category)
            #Flush the session (for possible rollback)
            db.session.flush()
            #Commit changes to database
            db.session.commit()
            #Redirect the admin back to admin category cms after successfully adding new category 
            return redirect("/admin_category_cms")
        #If request method is GET
        #render "admin_category_add" template
        return render_template("admin_category_add.html", flag=True)
    

#ROUTE FOR ADDING NEW PRODUCT IN ADMIN PRODUCT CMS
@app.route("/admin_product_add", methods=["GET", "POST"])
def admin_product_add():
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #If request method is POST, process the form submission to add a new product
        if request.method=="POST":
            #Get the product details from the form submitted by the admin
            product_name=request.form['product_name']
            product_category=request.form['product_category']
            product_brand=request.form['product_brand']
            product_mfg_date=request.form['product_mfg_date']
            product_exp_date=request.form['product_exp_date']
            product_unit=request.form['product_unit']
            product_qty=request.form['product_qty']
            product_price_per_unit=request.form['product_price_per_unit']
            password=request.form['password']
            #Get the uploaded file of image from the form submitted by the admin
            file = request.files['file']
            filename = None
            #Check if uploaded image file has allowed extension
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Query the Admin table in the database with the admin session ID and password
            #To verify the admin identity
            verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
            admin_check = [i for i in verify_admin]
            if admin_check:
                #If admin is verified and the file is successfully uploaded
                if filename is not None:
                    #set image path in image 
                    image = "/static/"+filename
            #Create a new Product with the provided product details
            new_product=Product(name=product_name, category=product_category, brand=product_brand, mfg_date=product_mfg_date, exp_date=product_exp_date, unit=product_unit, qty=product_qty, price_per_unit=product_price_per_unit, image=image)
            #Add new Product to the database session
            db.session.add(new_product)
            #Flush the session (for possible rollback)
            db.session.flush()
            #Commit changes to database
            db.session.commit()
            #Redirect the admin back to admin product cms after successfully adding new product
            return redirect("/admin_product_cms")
        #If request method is GET
        #render "admin_product_add" template
        return render_template("admin_product_add.html", flag=True)
    

#ROUTE FOR EDITING A SPECIFIC CATEGORY IN ADMIN CMS
@app.route("/admin_category_edit/<int:id>")
def admin_category_edit(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Query the category with the specified 'id' from the Category table in the database
        category = Category.query.filter_by(id=id)
        #Convert the query result to a list
        check = [i for i in category]
        #Render "admin_category_edit" template with the "category_info" variable containing the details of the category to be edited
        return render_template("admin_category_edit.html", category_info=check[0], flag=True)
    else:
        #If "admin_id" key not exists in session
        #redirect the user back to admin sign-in page to handle authentication before accessing the category editing page
        return redirect("/admin_sign-in")


#ROUTE FOR UPDATING A SPECIFIC CATEGORY IN ADMIN CMS
@app.route("/admin_category_update/<int:id>", methods=["POST"])
def admin_category_update(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Get the updated category details from the form submitted by the admin
        category_name = request.form.get("category_name")
        password = request.form.get("password")
        #Get the uploaded image file from the form submitted by the admin
        file = request.files['file']
        filename = None
        #Check if uploaded image file has allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #Querying the Admin table in the database with the admin's session ID and password
        #To verify the admin identity
        verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
        admin_check = [i for i in verify_admin]
        #Query the category with the specified "id" from the Category table in the database
        category = Category.query.filter_by(id=id)
        check = [i for i in category]
        if admin_check:
            #If the admin is verified and an image was uploaded, update the category name
            check[0].name = category_name
            if filename is not None:
                #sets the image path
                check[0].image = "/static/"+filename
            #Flush the session to save the changes
            db.session.flush()
            #Commit the changes to the database
            db.session.commit()
            flash("Category updated succesfully!")
            #Redirect the admin back to admin category cms after successfully updating the category
            return redirect("/admin_category_cms")
        else:
            #If admin is not verified, return "Wrong Password"
            return "Wrong Password!"
    else:
        #If "admin_id" key not exists in the session
        #redirect the user back to admin sign-in page to handle authentication before accessing the category update functionality 
        return redirect("/admin_sign-in")


#ROUTE FOR EDITING A SPECIFIC PRODUCT IN ADMIN CMS
@app.route("/admin_product_edit/<int:id>")
def admin_product_edit(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Query the product with the specified 'id' from the Product table in the database
        product = Product.query.filter_by(id=id)
        #Convert the query result to a list
        check = [i for i in product]
        #Render "admin_product_edit" template with the "product_info" variable containing the details of the product to be edited
        return render_template("admin_product_edit.html", product_info=check[0], flag=True)
    else:
        #If "admin_id" key not exists in session
        #redirect the user back to admin sign-in page to handle authentication before accessing the product editing page
        return redirect("/admin_sign-in")
    

#ROUTE FOR UPDATING A SPECIFIC PRODUCT IN ADMIN CMS
@app.route("/admin_product_update/<int:id>", methods=["POST"])
def admin_product_update(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Get the updated product details from the form submitted by the admin
        name = request.form.get("product_name")
        brand = request.form.get("product_brand")
        mfg_date = request.form.get("product_mfg_date")
        exp_date = request.form.get("product_exp_date")
        unit = request.form.get("product_unit")
        quantity = request.form.get("product_qty")
        price = request.form.get("product_price_per_unit")
        password = request.form.get("password")
        #Get the uploaded image file from the form submitted by the admin
        file = request.files['file']
        filename = None
        #Check if uploaded image file has allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #Querying the Admin table in the database with the admin's session ID and password
        #To verify the admin identity
        verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
        admin_check = [i for i in verify_admin]
        #Query the product with the specified "id" from the Product table in the database
        product = Product.query.filter_by(id=id)
        check = [i for i in product]
        if admin_check:
            #If the admin is verified and an image was uploaded, update the product name
            check[0].name = name
            check[0].brand = brand
            check[0].mfg_date = mfg_date
            check[0].exp_date = exp_date
            check[0].unit = unit
            check[0].qty = quantity
            check[0].price_per_unit = price
            if filename is not None:
                #sets the image path
                check[0].image = "/static/"+filename
            #Flush the session to save the changes
            db.session.flush()
            #Commit the changes to the database
            db.session.commit()
            flash("Product updated succesfully!")
            #Redirect the admin back to admin product cms after successfully updating the product
            return redirect("/admin_product_cms")
        else:
            #If admin is not verified, return "Wrong Password"
            return "Wrong Password!"
    else:
        #If "admin_id" key not exists in the session
        #redirect the user back to admin sign-in page to handle authentication before accessing the product update functionality 
        return redirect("/admin_sign-in")

#ROUTE FOR DELETING A SPECIFIC CATEGORY IN ADMIN CMS
@app.route("/admin_category_delete/<int:id>")
def admin_category_delete(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Delete all products associated with the category to be deleted
        Product.query.filter_by(category=id).delete()
        #Delete the category with the specified "id" from the Category table in the database
        Category.query.filter_by(id=id).delete()
        #Flush the session to save the changes
        db.session.flush()
        #Commit the changes to database
        db.session.commit()
        flash("Category deleted successfully!")
    #Redirect the admin back to admin_category_cms page after successfully deleting the category
    return redirect("/admin_category_cms")
    

#ROUTE FOR DELETING A SPECIFIC PRODUCT IN ADMIN CMS
@app.route("/admin_product_delete/<int:id>")
def admin_product_delete(id):
    #Check if "admin_id" key exists in session
    if "admin_id" in session:
        #Delete the product with the specified "id" from the Product table in the database
        Product.query.filter_by(id=id).delete()
        #Flush the session to save the changes
        db.session.flush()
        #Commit the changes to database
        db.session.commit()
        flash("Product deleted successfully!")
    #Redirect the admin back to admin_product_cms page after successfully deleting the product
    return redirect("/admin_product_cms")


@app.route("/admin_search")
def admin_search():
    #request.arg.get() is used to retrieve query parameters from the URL
    #Query parameters added to the URL after "?" symbol & used for GET requests
    input_query = request.args.get("query")
    if input_query:
        #Check if input query matches any category name
        category_results = Category.query.filter(Category.name.ilike(f"%{input_query}%")).all()

        if category_results:
            #If there are category matches, display products under the first matched category
            category_id = category_results[0].id
            products_in_category = Product.query.filter_by(category=category_id).all()
            return render_template("admin_search.html", query=input_query, results=products_in_category, flag=True)

        #If no category matches, search for products matching the input query
        product_results = Product.query.filter(
            db.or_(
                Product.name.ilike(f"%{input_query}%"),
                Product.brand.ilike(f"%{input_query}%"),
            )
        ).all()

        if product_results:
            return render_template("admin_search.html", query=input_query, results=product_results, flag=True)

    return render_template("admin_search.html", query=input_query, results=None, flag=True)




