from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nba_players.db')
app.secret_key = os.urandom(24)  # This is needed for session handling

db = SQLAlchemy(app)

class NBAPlayers(db.Model):
    __tablename__ = 'nba_players'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String)
    player_id = db.Column(db.Integer)
    picture_path = db.Column(db.String)
    player_worth = db.Column(db.Integer)
    image = db.Column(LargeBinary)

@app.route("/", methods=["GET", "POST"])
def front_page():
    if request.method == "POST" and request.is_json:
        searchbox = request.json.get("text")
        players = NBAPlayers.query.filter(NBAPlayers.player_name.like(f"%{searchbox}%")).all()
        result = [{
            "player_name": player.player_name, 
            "player_id": player.player_id,
            "player_worth": player.player_worth
        } for player in players]
        return jsonify(result)
    return render_template("trade.html")

@app.route("/analysis", methods=['GET', 'POST'])
def show_analysis():
    if request.method == 'POST':
        data = request.json
        left_players = data.get('left', [])
        right_players = data.get('right', [])

        print(f"POST data received. Left players: {left_players}, Right players: {right_players}")

        # Store the player IDs in the session
        session['left_players'] = left_players
        session['right_players'] = right_players
        
        return jsonify({'redirect': url_for('show_analysis')})
    
    else:  # GET request
        left_players = session.get('left_players', [])
        right_players = session.get('right_players', [])
        
        print(f"GET session data. Left players: {left_players}, Right players: {right_players}")

        if not left_players or not right_players:
            print("No player data found in session.")
        
        left_team = NBAPlayers.query.filter(NBAPlayers.player_id.in_(left_players)).all()
        right_team = NBAPlayers.query.filter(NBAPlayers.player_id.in_(right_players)).all()

        print(f"Left team data: {[player.player_name for player in left_team]}")
        print(f"Right team data: {[player.player_name for player in right_team]}")

        left_worth = round(sum(player.player_worth for player in left_team),2)
        right_worth = round(sum(player.player_worth for player in right_team),2)
        
        print(f"Calculated worth. Left worth: {left_worth}, Right worth: {right_worth}")
        
        if left_worth > right_worth:
            winner = 'left'
        elif right_worth > left_worth:
            winner = 'right'
        else:
            winner = 'tie'
        
        
        return render_template("analysis.html", left_team=left_team, right_team=right_team, 
                               left_worth=left_worth, right_worth=right_worth, winner=winner)

@app.route("/modify-trade", methods=["GET", "POST"])
def modifyTrade():
    if request.method == "POST":
        # Handle updating the trade
        data = request.json
        left_players = data.get('left', [])
        right_players = data.get('right', [])
        
        # Update the session data
        session['left_players'] = [player['playerID'] for player in left_players]
        session['right_players'] = [player['playerID'] for player in right_players]
        
        return jsonify({'redirect': url_for('/analysis')})
    else:
        # Render the modify trade page
        return render_template("trade.html")

if __name__ == "__main__":
    app.run(debug=True)
