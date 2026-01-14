from app import db

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    addr = db.Column(db.String(120))
    pin = db.Column(db.String(20))

    def __repr__(self):
        return f'<Etudiant {self.nom}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'addr': self.addr,
            'pin': self.pin
        }


def init_db():
    db.create_all()


def ajouter_etudiant(nom, addr, pin):
    e = Etudiant(nom=nom, addr=addr, pin=pin)
    db.session.add(e)
    db.session.commit()


def get_etudiants():
    return Etudiant.query.all()


def update_etudiant(id, addr, pin):
    e = Etudiant.query.get(id)
    if e:
        e.addr = addr
        e.pin = pin
        db.session.commit()