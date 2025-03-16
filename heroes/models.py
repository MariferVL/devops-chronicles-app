from app import db 

class Hero(db.Model):
    __tablename__ = 'heroes'  

    # Define the table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    health = db.Column(db.Integer, default=100)  # Represents the hero's resilience
    automation = db.Column(db.Integer, default=50)  # Level of automation skills
    experience = db.Column(db.Integer, default=0)  # Initial experience
    integrity = db.Column(db.Integer, default=50)  # Adherence to best practices

    def __repr__(self):
        return f"<Hero {self.name}, Role: {self.role}>"

    def to_dict(self):
        """Converts the model to a dictionary for a JSON response."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "health": self.health,
            "automation": self.automation,
            "experience": self.experience,
            "integrity": self.integrity
        }
