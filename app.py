from flask import Flask
from flask import flash,session,redirect,url_for,escape,request,render_template,Markup,abort
import os,datetime

app = Flask(__name__)

from controllers.Utils import Utils
from controllers.Snippet import Snippet
from controllers.Note import Note
from controllers.Upload import Upload

from config import SECRET_KEY,USERNAME,PASSWORD

app.jinja_env.filters['datetime'] = Utils.formatDate
app.secret_key = SECRET_KEY


# - Media files
@app.route('/media')
def media():
    #  check user session
    if 'username' in session and 'secretkey' in session:
        try:
            data = {
                "img": Upload.all('static/uploads')
            }
        except Exception as e:
            data = {"img": ""}
            flash(e)
        finally:
            tpl = 'views/media.html'
            return render_template(tpl,data=data)
    # no session go to login page
    return abort(404)

@app.route('/media/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            f = request.files['the_file']
            return Upload.add(f)
    return abort(404)

@app.route('/media/delete', methods=['GET', 'POST'])
def delete_file():
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            filename = request.form['file']
            return Upload.delete(filename)
    return abort(404)

# ----------------------------------

# - Snippets
@app.route('/snippets')
def snippets():
    #  check user session
    if 'username' in session and 'secretkey' in session:
        tpl = 'views/snippets.html'
        return render_template(tpl,rows = Snippet.all())
    # no session go to login page
    return abort(404)

@app.route("/snippets/new",methods = ['POST', 'GET'])
def newSnippet():
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            return Snippet.add()
        else:
            return redirect(url_for('snippets'))
    return abort(404)

@app.route("/snippets/update/<int:num>/",methods = ['POST'])
def updateSnippet(num):
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            return Snippet.put(num)
    return abort(404)

@app.route("/snippets/edit/<int:num>/")
def editSnippet(num=47):
    if 'username' in session and 'secretkey' in session:
        tpl = 'views/snippets_edit.html'
        return Snippet.get(tpl,num)
    return abort(404)

@app.route("/snippets/preview/<int:num>/")
def previewSnippet(num):
    tpl = 'views/snippets_sandbox.html'
    return Snippet.get(tpl,num)


@app.route("/snippets/delete/<int:num>/")
def deleteSnippet(num):
    if 'username' in session and 'secretkey' in session:
        try:
            return Snippet.delete(num)
        except Exception:
            flash('The file is not removed!')
        finally:
            flash('The file has been removed!')
    return abort(404)

# ----------------------------------

# - Notes
@app.route('/notes')
def notes():
    #  check user session
    if 'username' in session and 'secretkey' in session:
        tpl = 'views/notes.html'
        return render_template(tpl,rows=Note.all())
    # no session go to login page
    return abort(404)

@app.route("/notes/new",methods = ['POST', 'GET'])
def newNote():
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            return Note.add()
        else :
            tpl = 'views/notes_new.html'
            return render_template(tpl)
    return abort(404)

@app.route("/notes/edit/<int:num>/",methods = ['POST','GET'])
def editNote(num):
    if 'username' in session and 'secretkey' in session:
        if request.method == 'POST':
            return Note.edit()
        else :
            tpl = 'views/notes_edit.html'
            return render_template(tpl,data=Note.get(num))
    return abort(404)

@app.route("/notes/delete/<int:num>/")
def deleteNote(num):
    if 'username' in session and 'secretkey' in session:
        try:
            return Note.delete(num)
        except Exception:
            flash('The note is not removed!')
        finally:
            flash('The note has been removed!')
    return abort(404)
        
# ----------------------------------

# - Home
@app.route('/')
@app.route('/index')
def index():
    if 'username' in session and 'secretkey' in session:
        data = {
            "username":session['username']
        }
        tpl = 'views/index.html'
        return render_template(tpl,data=data)
    else: 
        return redirect(url_for('login'))

# - Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:

            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['secretkey'] = SECRET_KEY

            flash('User is logged')
            return redirect(url_for('index'))
        else :
            flash('Error The user not exists')
            return redirect(url_for('login'))
    tpl = 'views/login.html'
    return render_template(tpl,msg=msg)

# - Logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('The user is out from system')
    return redirect(url_for('index'))

# - Error
@app.errorhandler(404)
def not_found(error):
    tpl = 'views/error.html'
    return render_template(tpl), 404


# ----------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

