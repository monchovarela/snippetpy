from flask import Flask
from flask import flash,session,redirect,url_for,escape,request,render_template,Markup,abort
import os,datetime

app = Flask(__name__)

from controllers.api import Api

app.jinja_env.filters['datetime'] = Api.formatDate

####################################
# - Upload files                   #
####################################
@app.route('/media/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        return Api.upload_new(f)
####################################
# - Media  files                   #
####################################
@app.route('/media/delete', methods=['GET', 'POST'])
def delete_file():
    if request.method == 'POST':
        filename = request.form['file']
        return Api.upload_delete(filename)
####################################
# - Snippets                       #
####################################
@app.route("/snippets")
def snippetsView():
    return render_template(
            "views/snippets.html",
            rows = Api.snippets_get_all()
        )
####################################
# - Snippets new                   #
####################################
@app.route("/snippets/new",methods = ['POST', 'GET'])
def newSnippet():
    if request.method == 'POST':
        return Api.snippets_new()
    else:
        return redirect(url_for('snippets'))
####################################
# - Snippets update                #
####################################
@app.route("/snippets/update/<int:num>/",methods = ['POST'])
def updateSnippet(num):
    if request.method == 'POST':
        return Api.snippets_update(num)
####################################
# - Snippets edit                  #
####################################
@app.route("/snippets/edit/<int:num>/")
def editSnippet(num=47):
    return Api.snippets_get_uid('views/snippets_edit.html',num)
####################################
# - Snippets preview               #
####################################
@app.route("/snippets/preview/<int:num>/")
def previewSnippet(num):
    return Api.snippets_get_uid('views/snippets_sandbox.html',num)
####################################
# - Snippets delete                #
####################################
@app.route("/snippets/delete/<int:num>/")
def deleteSnippet(num):
    try:
        return Api.snippets_delete_uid(num)
    except Exception:
        flash('The file is not removed!')
    finally:
        flash('The file has been removed!')
####################################
# - Notes new                      #
####################################
@app.route("/notes/new",methods = ['POST', 'GET'])
def newNote():
    if request.method == 'POST':
        return Api.notes_new()
    else :
        return redirect(url_for('notes'))
####################################
# - Notes edit                     #
####################################
@app.route("/notes/edit/<int:num>/",methods = ['POST','GET'])
def editNote(num):
    if request.method == 'POST':
        return Api.notes_edit()
    else :
        return render_template(
                'views/notes_edit.html',
                data=Api.notes_get_uid(num)
            )
####################################
# - Notes delete                   #
####################################
@app.route("/notes/delete/<int:num>/")
def deleteNote(num):
    try:
        return Api.notes_delete_uid(num)
    except Exception:
        flash('The note is not removed!')
    finally:
        flash('The note has been removed!')
        


############################
# - Home                   #
############################
@app.route('/')
@app.route('/index')
def index():
    #  check user session
    if 'username' in session:
        data = {
            "username":session['username'],
        }
        return render_template('views/index.html',data=data)
    # no session go to login page
    return redirect(url_for('login'))
############################
# - Media                  #
############################
@app.route('/media')
def media():
    #  check user session
    if 'username' in session:
        try:
            data = {
                "img": Api.upload_get_all('static/uploads')
            }
        except Exception as e:
            data = {"img": ""}
            flash(e)
        finally:
            return render_template('views/media.html',data=data)
    # no session go to login page
    return redirect(url_for('login'))
############################
# - Notes                  #
############################
@app.route('/notes')
def notes():
    #  check user session
    if 'username' in session:
        return render_template('views/notes.html',rows=Api.notes_get_all())
    # no session go to login page
    return redirect(url_for('login'))
############################
# - Snippets               #
############################
@app.route('/snippets')
def snippets():
    #  check user session
    if 'username' in session:
        data = {}
        return render_template('views/snippets.html',data=data)
    # no session go to login page
    return redirect(url_for('login'))
############################
# - Login                  #
############################
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'demo123':
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            flash('User is logged')
            return redirect(url_for('index'))
        else :
            flash('Error The user not exists')
            return redirect(url_for('login'))
    return render_template('views/login.html',msg=msg)
############################
# - Logout                 #
############################
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('The user is out from system')
    return redirect(url_for('index'))
############################
# - Error                  #
############################
@app.errorhandler(404)
def not_found(error):
    return render_template('views/error.html'), 404

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

