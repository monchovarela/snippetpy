from flask import flash,request,redirect,url_for
import os,sqlite3

from config import DB_NOTES

# Note
class Note:

    @staticmethod
    def add():
        try:
            name = request.form['title'].replace(' ', '-').lower()
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']
            with sqlite3.connect(DB_NOTES) as db:
                c = db.cursor()
                sql = 'INSERT INTO notes (name,title,desc,date) VALUES (?,?,?,?)'
                c.execute(sql,(name,title,desc,date) )
                db.commit()
                flash('Success, the note is added')
        except:
            db.rollback()
            flash('Error, maybe the title already exists!')
        finally:
            db.close()
            return redirect(url_for('notes'))

    @staticmethod
    def edit():
        try:
            uid = request.form['uid']
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']
            with sqlite3.connect(DB_NOTES) as db:
                cursor = db.cursor()
                sql = 'UPDATE notes SET title = ?,desc = ?,date = ? WHERE uid = ?'
                cursor.execute(sql,(title,desc,date,uid) )
                db.commit()
                flash('The Note has been update!')
                return redirect(url_for('notes'))
        except:
            db.rollback()
            flash('Error on update Note')
            return redirect(url_for('notes'))
        finally:
            db.close()
            flash('The Note has been update!')
            return redirect(url_for('notes'))

    @staticmethod
    def get(uid):
        t = (uid,)
        with sqlite3.connect(DB_NOTES) as db:
            db = sqlite3.connect(DB_NOTES)
            db.row_factory = sqlite3.Row # para poder usar dot notacion
            cursor = db.cursor()
            cursor.execute("SELECT uid,name,title,desc,date FROM notes WHERE UID=?",t)
            rows = cursor.fetchone()
            cursor.close()
            return rows

    @staticmethod
    def all():
        with sqlite3.connect(DB_NOTES) as db:
            db.row_factory = sqlite3.Row # para poder usar dot notacion
            cursor = db.cursor()
            cursor.execute("SELECT uid,name,title,desc,date FROM notes")
            rows = cursor.fetchall()
            cursor.close()
            return rows

    @staticmethod
    def delete(uid):
        t = (uid,)
        with sqlite3.connect(DB_NOTES) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM notes WHERE uid=?",t)
            db.commit()
            cursor.close()
            flash('The Note has been deleted!')
            return redirect(url_for('notes'))
