from flask import Flask, render_template, request, redirect, url_for
from data import read_glams_by_glam_type, read_glam_by_glam_id, insert_glam, delete_glam, update_glam

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Add route to list of glams 
@app.route('/places/<glam_type>')
def places(glam_type):
    glams_list = read_glams_by_glam_type(glam_type)
    return render_template("places.html", glam_type=glam_type, glams=glams_list)

# Retrieves 1 glam by glam_id
@app.route('/places/<int:glam_id>')
def glam(glam_id):
    glam = read_glam_by_glam_id(glam_id)
    return render_template("glam.html", glam=glam)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processed', methods=['post'])
def processing():
    glam_data = { 
        "glam_type": request.form['glam_type'],
        "name": request.form['glam_name'],
        "date_established": request.form['glam_date_established'],
        "location": request.form['glam_location'],
        "description": request.form['glam_desc'],
        "url": request.form['glam_url']
    }
    insert_glam(glam_data)
    return redirect(url_for('places', glam_type=request.form['glam_type']))

@app.route('/modify', methods=['post'])
def modify():
    # 1. identify whether user clicked edit or delete
       # if edit, then do this:
    if request.form["modify"] == "Edit":
        # retrieve record using id
        glam_id = request.form["glam_id"] 
        glam = read_glam_by_glam_id(glam_id)
        # update record with new data
        return render_template('update.html', glam=glam, glam_type=glam['glam_type'])
    # if delete, then do this
    elif request.form["modify"] == "Delete":
        # retrieve record using id
        glam_id = request.form["glam_id"]
        # delete the record
        delete_glam(glam_id)
        # redirect user to glam list by glam type
    return redirect(url_for('places', glam_type=request.form.get('glam_type', '')))

@app.route('/update', methods=['post'])
def update():
    glam_data = {
        "glam_id": request.form['glam_id'],
        "glam_type": request.form['glam_type'],
        "name": request.form['glam_name'],
        "date_established": request.form['glam_date_established'],
        "location": request.form['glam_location'],
        "description": request.form['glam_desc'],
        "url": request.form['glam_url']
    }
    update_glam(glam_data)
    return redirect(url_for('glam', glam_id=request.form['glam_id']))


if __name__ == "__main__":
    app.run(debug=True)