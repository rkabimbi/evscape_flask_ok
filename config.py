import os, binascii

basedir= os.path.abspath(os.path.dirname(__file__))#on définit un objet que l'on peut recuperer ensuite pour eviter de devoir taper tout le path depuis la racine du pc

class BaseConfig(object):
    #UPLOAD_FOLDER = '/Users/rudykabimbingoy/Documents/DEVELOPEMENT/_MEMOIRE/eVscape_flask_ok/X_UPLOAD_FOLDER'
    UPLOAD_FOLDER = '/Users/rudykabimbingoy/Documents/DEVELOPEMENT/_MEMOIRE/eVscape_flask_ok/my_app/static/img'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = binascii.hexlify(os.urandom(24))  
    DEBUG=True
    ENV="development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'db','EvscapeDB.db')#basedir pour dire on part du truc de base et ensuite il trouvera le fichier db qui s'appelle enigmes.db dans le dossier "db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False#pour voir si sql doit guetter les changement
    TEMPLATES_AUTO_RELOAD = True #si je change du html et ce que ca doit etre relaodé (oui c'est bcp plus pratique)

