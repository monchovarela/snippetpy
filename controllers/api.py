from flask import Markup,render_template,flash,request,redirect,url_for
import os,datetime,time,sqlite3

db_code = "storage/code.db"
db_notes = "storage/notes.db"
uploads_folder = "static/uploads"

class Api:
    
    @staticmethod
    def formatDate(t):
        return datetime.datetime.fromtimestamp(int(t)).strftime('%d-%m-%Y')
    ###################################
    # Uploads
    ###################################
    @staticmethod
    def upload_get_all(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file
    @staticmethod
    def upload_new(f):
        filetypes = (
            '.png', '.jpg', '.jpeg',
            'gif','.zip','.html','.css',
            '.js','.wav','.mp3','.mp4','.webm'
        )
        if f.filename.lower().endswith(filetypes):
            fileurl = os.path.join(uploads_folder,f.filename)
            f.save(fileurl)
            if(os.path.isfile(fileurl)):
                flash('The file has been uploaded!')
                return redirect(url_for('media'))
            else:
                flash('Sorry the file is not uploaded')
                return redirect(url_for('media'))
        else :
            flash('Sorry only images are support')
            return redirect(url_for('media'))
    @staticmethod
    def upload_delete(filename):
        fileurl = os.path.join(uploads_folder,filename)
        if(os.path.isfile(fileurl)):
            os.remove(fileurl)
            flash('The file has been removed!')
            return redirect(url_for('media'))
        else :
            flash('The file not exists')
            return redirect(url_for('media'))
    ###################################
    # Snippets
    ###################################
    @staticmethod
    def snippets_new():
        try:
            name = request.form['title'].replace(' ', '-').lower()
            title = request.form['title']
            desc = request.form['desc']
            date = time.time()  

            with sqlite3.connect(db_code) as db:
                c = db.cursor()

                sql = '''INSERT INTO code
                    (name,title,desc,date)
                    VALUES (?,?,?,?)'''

                c.execute(sql,(name,title,desc,date) )
                db.commit()
        except:
            db.rollback()
            flash('Error in insert operation')
        finally:
            db.close()
            return redirect(url_for('snippets'))
    @staticmethod
    def snippets_update(uid):
        db = sqlite3.connect(db_code)
        try:
            req = request.json
            html = req.get('html')
            css = req.get('css')
            js = req.get('javascript')
            title = req.get('title')
            desc = req.get('desc')
            
            cursor = db.cursor()
            sql = '''UPDATE code SET title = ?,desc = ?,html = ? ,css = ? ,javascript = ? WHERE uid = ?'''
            cursor.execute(sql,(title,desc,html,css,js,uid))

            db.commit()
        except:
            db.rollback()
            return '{"status":false}'
        finally:
            return '{"status":true}'
            db.close()
    @staticmethod
    def snippets_get_uid(tpl,uid):
        # formato tupla
        t = (uid,)
        # conectamos la base de datos
        conn = sqlite3.connect(db_code)
        # cursor
        c = conn.cursor()
        # ejecutamos
        c.execute("SELECT * FROM code WHERE uid=?",t)
        # fetchone solo para un id
        config = c.fetchone()
        c.close()
        # si se resuelve enseñamos sino mandamos el 404
        if config :
            data = {
                "uid": config[0],
                "name": config[1],
                "title": config[2],
                "desc": Markup(config[3]),
                "html": Markup(config[4]),
                "javascript": Markup(config[5]),
                "css": config[6]
            }
            return render_template(tpl,data=data)
        else:
            return render_template('views/error.html')
    @staticmethod
    def snippets_get_all():
        db = sqlite3.connect(db_code)
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute("SELECT uid,name,title,desc,date FROM code")
        rows = cur.fetchall();
        cur.close()
        return rows
    @staticmethod
    def snippets_delete_uid(uid):
        t = (uid,)
        db = sqlite3.connect(db_code)
        c = db.cursor()
        c.execute("DELETE FROM code WHERE uid=?",t)
        db.commit()
        c.close()
        return redirect(url_for('snippets'))
    ###################################
    # Notes
    ###################################
    @staticmethod
    def notes_new():
        try:

            name = request.form['title'].replace(' ', '-').lower()
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']

            with sqlite3.connect(db_notes) as db:
                c = db.cursor()

                sql = '''INSERT INTO notes
                    (name,title,desc,date)
                    VALUES (?,?,?,?)'''

                c.execute(sql,(name,title,desc,date) )
                db.commit()
                flash('Success, the note is added')
        except:
            db.rollback()
            flash('Error in insert operation')
        finally:
            return redirect(url_for('notes'))
            db.close()
    @staticmethod
    def notes_edit():
        try:
            uid = request.form['uid']
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']

            with sqlite3.connect(db_notes) as db:
                c = db.cursor()
                sql = '''UPDATE notes SET title = ?,desc = ?,date = ? WHERE uid = ?'''
                c.execute(sql,(title,desc,date,uid) )
                db.commit()

                flash('Success, the note is update')
        except:
            db.rollback()
            flash('Error in update operation')
        finally:
            return redirect(url_for('notes'))
            db.close()
    @staticmethod
    def notes_get_uid(uid):
        t = (uid,)
        db = sqlite3.connect(db_notes)
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute("SELECT uid,name,title,desc,date FROM notes WHERE UID=?",t)
        rows = cur.fetchone();
        cur.close()
        return rows
    @staticmethod
    def notes_get_all():
        db = sqlite3.connect(db_notes)
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute("SELECT uid,name,title,desc,date FROM notes")
        rows = cur.fetchall();
        cur.close()
        return rows
    @staticmethod
    def notes_delete_uid(uid):
        t = (uid,)
        db = sqlite3.connect(db_notes)
        c = db.cursor()
        c.execute("DELETE FROM notes WHERE uid=?",t)
        db.commit()
        c.close()
        return redirect(url_for('notes'))