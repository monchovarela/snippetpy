from flask import flash,redirect,url_for,session
import os,re,datetime,time,sqlite3

###################################
# Utils
###################################
class Utils:
    
    @staticmethod
    def formatDate(t):
        return datetime.datetime.fromtimestamp(int(t)).strftime('%d-%m-%Y')

    @staticmethod
    def redirect(title,where):
        flash(title)
        return redirect(url_for(where))

    @staticmethod
    def slugify(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)
        

