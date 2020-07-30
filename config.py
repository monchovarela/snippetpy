import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))

DB_NOTES = os.path.join(BASEDIR, 'storage/notes.db')
DB_SNIPPETS = os.path.join(BASEDIR, 'storage/code.db')
UPLOADS = os.path.join(BASEDIR, 'static/uploads')

#Security configuration
CSRF_ENABLED = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
USERNAME = 'admin'
PASSWORD = 'demo123'


