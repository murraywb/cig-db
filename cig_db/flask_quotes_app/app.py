from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_quotes_app.config import Config

# Initialize Flask app and load config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Quotes Model (database table)
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    book = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.Text, nullable=False)
    submitted_by = db.Column(db.String(255), nullable=True)
    approved = db.Column(db.Boolean, default=False)
    submission_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    quotes = Quote.query.filter_by(approved=True).all()  # Show only approved quotes
    return render_template('index.html', quotes=quotes)

@app.route('/submit', methods=['GET', 'POST'])
def submit_quote():
    if request.method == 'POST':
        author = request.form['author']
        book = request.form['book']
        quote = request.form['quote']
        submitted_by = request.form['submitted_by'] or None

        new_quote = Quote(author=author, book=book, quote=quote, submitted_by=submitted_by)
        db.session.add(new_quote)
        db.session.commit()

        flash('Quote submitted! Waiting for approval.')
        return redirect(url_for('index'))

    return render_template('submit.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        quote_id = request.form['quote_id']
        action = request.form['action']

        quote = Quote.query.get(quote_id)
        if action == 'approve':
            quote.approved = True
        elif action == 'reject':
            db.session.delete(quote)

        db.session.commit()

    quotes = Quote.query.filter_by(approved=False).all()  # Show unapproved quotes
    return render_template('admin.html', quotes=quotes)

if __name__ == '__main__':
    app.run(debug=True)
