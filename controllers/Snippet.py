from flask import flash,request,redirect,url_for,render_template,Markup
import os,time,sqlite3

from config import DB_SNIPPETS
from controllers.Utils import Utils

# Snippet
class Snippet:

    @staticmethod
    def add():
        try:
            name = Utils.slugify(request.form['title'])
            title = request.form['title']
            desc = request.form['desc']
            date = time.time()  
            with sqlite3.connect(DB_SNIPPETS) as db:
                cursor = db.cursor()
                sql = 'INSERT INTO code (name,title,desc,date) VALUES (?,?,?,?)'
                cursor.execute(sql,(name,title,desc,date))
                db.commit()
                return redirect(url_for('snippets'))
        except:
            db.rollback()
            flash('Error in insert operation')
            return redirect(url_for('snippets'))
        finally:
            db.close()
            flash('The Snippet has been created!')
            return redirect(url_for('snippets'))

    @staticmethod
    def put(uid):
        try:
            req = request.json
            html = req.get('html')
            css = req.get('css')
            js = req.get('javascript')
            title = req.get('title')
            desc = req.get('desc')
            with sqlite3.connect(DB_SNIPPETS) as db:
                cursor = db.cursor()
                sql = 'UPDATE code SET title = ?,desc = ?,html = ? ,css = ? ,javascript = ? WHERE uid = ?'
                cursor.execute(sql,(title,desc,html,css,js,uid))
                db.commit()
        except:
            db.rollback()
            return '{"status":false}'
        finally:
            return '{"status":true}'
            db.close()

    @staticmethod
    def get(tpl,uid):
        t = (uid,)
        with sqlite3.connect(DB_SNIPPETS) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM code WHERE uid=?",t)
            config = cursor.fetchone()
            cursor.close()
        # si se resuelve enseñamos sino mandamos el 404
        if config:
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
    def all():
        with sqlite3.connect(DB_SNIPPETS) as db:
            db.row_factory = sqlite3.Row # para poder usar dot notacion
            cursor = db.cursor()
            cursor.execute("SELECT uid,name,title,desc,date FROM code")
            rows = cursor.fetchall()
            cursor.close()
            return rows

    @staticmethod
    def delete(uid):
        t = (uid,)
        with sqlite3.connect(DB_SNIPPETS) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM code WHERE uid=?",t)
            db.commit()
            cursor.close()
            return redirect(url_for('snippets'))
