from extensions import db 

class Adventure(db.Model):
    __tablename__ = 'adventures'  

    # Define the table columns
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)  
    challenge = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)
    experience_gain = db.Column(db.Integer, default=0)

    # Reverse relationship with Hero (a hero can have many adventures)
    hero = db.relationship('Hero', backref='adventures', lazy=True)

    def __repr__(self):
        return f"<Adventure for Hero {self.hero_id}, Challenge: {self.challenge}>"

    def to_dict(self):
        """Converts the model to a dictionary for a JSON response."""
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "challenge": self.challenge,
            "result": self.result,
            "experience_gain": self.experience_gain
        }
