from flask import flash,redirect,url_for
import os

from config import UPLOADS
from controllers.Utils import Utils

# Upload
############
class Upload:
    
    @staticmethod
    def all(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    @staticmethod
    def add(f):
        filetypes = (
            '.png', '.jpg', '.jpeg','gif',
            '.zip','.html','.css','.js',
            '.wav','.mp3',
            '.mp4','.webm',
            'pdf','docx','doc'
        )
        if f.filename.lower().endswith(filetypes):
            fileurl = os.path.join(UPLOADS,Utils.slugify(f.filename))
            f.save(fileurl)
            if(os.path.isfile(fileurl)):
                flash('The file has been uploaded!')
                return redirect(url_for('media'))
            else:
                flash('Sorry the file is not uploaded')
                return redirect(url_for('media'))
        else:
            flash('Sorry we can not accept this file type')
            return redirect(url_for('media'))

    @staticmethod
    def delete(filename):
        fileurl = os.path.join(UPLOADS,filename)
        if(os.path.isfile(fileurl)):
            os.remove(fileurl)
            flash('The file has been removed!')
            return redirect(url_for('media'))
        else:
            flash('The file not exists')
            return redirect(url_for('media'))
