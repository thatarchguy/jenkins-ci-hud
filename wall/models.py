from wall import db
import datetime


class ContinuousBuilds(db.Model):
    """
    Database model for CI builds
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    phase =  db.Column(db.String(50))
    status =  db.Column(db.String(50))
    sourceBranch =  db.Column(db.String(50))
    targetBranch = db.Column(db.String(50))
    full_url = db.Column(db.String(144))
    date_added = db.Column(db.String(20))
    date_modified = db.Column(db.String(20))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Deployments(db.Model):
    """
    Database model for Deployments
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    phase =  db.Column(db.String(50))
    status =  db.Column(db.String(50))
    sourceBranch =  db.Column(db.String(50))
    full_url = db.Column(db.String(144))
    date_added = db.Column(db.String(20))
    date_modified = db.Column(db.String(20))

    def __repr__(self):
        return '<build %r>' % (self.number)
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}