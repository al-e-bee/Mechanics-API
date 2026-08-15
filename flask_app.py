from flask import redirect
from app import create_app
from app.models import db

app = create_app('ProductionConfig')
  
with app.app_context():
    # db.drop_all()
    db.create_all()
    
@app.route('/')
def home():
    return redirect('/api/docs/')
    
if __name__=='__main__':
    app.run()