from flask_login import UserMixin
from my_app import login_manager
from my_app import db #importe l'objet DB cree dans le init.py
from werkzeug.security import generate_password_hash, check_password_hash #pour generer le password
from datetime import datetime#pour le timestamp du message


from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from my_app.models.riddle import Enigmes#si je ne fais pas ça alors il ne sait pas acceder à la foreginkey!!!!!!!


class Clue( db.Model):
    
    __tablename__ = 'indice' 
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)#on crée une colonne à la table (un attribut), on donne le type, on dit que c'est une clé primaire, et qu'il  ya un incrmeent autmatique
    indice = db.Column(db.String(200))
    enigme_id = db.Column(db.Integer, db.ForeignKey('enigme.id'), nullable=False)#on crée une colonne dans la table qui contient la clée etrangere user.id

    def __repr__(self):#toString
        return "(id=%i, indice = %s)\n" % (self.id, self.indice)


    def __init__(self,indice,enigme_id):
            self.indice=indice
            self.enigme_id = enigme_id
    

db.create_all()#impératif!!!!!!

