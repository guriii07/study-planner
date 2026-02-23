from app import db
from datetime import datetime

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # We store the Gemini JSON output as a text string in the database
    schedule_json = db.Column(db.Text, nullable=False) 

    def __repr__(self):
        return f"<StudyPlan {self.exam_name}>"