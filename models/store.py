from db import db



class StoreModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel")

    def __init__(self, name, price):
        self.name = name
        
    
    def json(self):
        return {"name": self.name, "items":[
            item.json() for item in self.items

        ]
        }


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()     
    
    
    
    def delete_from_db(self):
        db.session.delete(self)



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()