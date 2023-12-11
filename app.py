from flask import Flask, render_template, request, redirect, jsonify
from database import engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models import Game, Team, Player
import mysql.connector
import os

db = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE']
)

app = Flask(__name__)

Session = sessionmaker(bind=engine)

@app.route('/delete_game', methods=['POST'])
def delete_game():
  try:
    # Get the selected game ID from the request data
    data = request.get_json()
    selected_game_id = data.get('game_id')

    print("Selected Game ID:", selected_game_id)

    # Perform the deletion using a prepared statement
    with db.cursor() as cursor:
        sql = "DELETE FROM game WHERE game_id = %s"
        cursor.execute(sql, (selected_game_id,))
        db.commit()
    return redirect('/')
    
    return jsonify({'message': 'Game deleted successfully'}), 200

  except Exception as e:
    # Log the error for debugging
    print(f"Error deleting game: {e}")
    return jsonify({'message': 'Failed to delete game. Please try again.'}), 500

@app.route('/edit_game', methods=['POST'])
def edit_game():
    if request.method == 'POST':
        try:
            # Retrieve form data, including gameId
            game_id = request.form.get('gameId')
            date = request.form.get('date')
            home_team = request.form.get('homeTeam')
            home_city = request.form.get('homeCity')
            away_team = request.form.get('awayTeam')
            away_city = request.form.get('awayCity')
            location = request.form.get('location')
            outcome = request.form.get('outcome')

            print(f"Received game_id: {game_id}")
            # Create a cursor object
            cursor = db.cursor()

            # Define the SQL update query with placeholders
            update_query = """
                UPDATE game 
                SET date = %s, homeTeam = %s, homeCity = %s, awayTeam = %s, awayCity = %s, location = %s, outcome = %s 
                WHERE game_id = %s
            """

            # Execute the SQL query with the data and gameId as parameters
            cursor.execute(update_query, (date, home_team, home_city, away_team, away_city, location, outcome, game_id))

            session = Session()
            existing_home_team = session.query(Team).filter_by(name=home_team).first()
            if not existing_home_team:
                # Create a new Team object for the home team
                new_home_team = Team(name=home_team, city=home_city)
                session.add(new_home_team)

            # Check if the away team exists in the team table
            existing_away_team = session.query(Team).filter_by(name=away_team).first()
            if not existing_away_team:
                # Create a new Team object for the away team
                new_away_team = Team(name=away_team, city=away_city)
                session.add(new_away_team)

            
            # Commit the changes to the database
            session.commit()
            db.commit()

            # Close the cursor
            session.close()
            cursor.close()

            # Redirect to the game stats page or a confirmation page
            return redirect('/')

        except Exception as e:
            # Handle any exceptions, e.g., by displaying an error message
            # Log the error for debugging
            print(f"Error deleting game: {e}")
            return jsonify({'message': 'Failed to delete game. Please try again.'}), 500

    # Handle other HTTP methods or invalid requests
    return "Invalid request."

def load_games_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM game"))
    games = []
    column_names = result.keys()
    for row in result.all(): 
      games.append(dict(zip(column_names, row)))
    return games
    
def load_teams_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM team"))
    teams = []
    column_names = result.keys()
    for row in result.all(): 
      teams.append(dict(zip(column_names, row)))
    return teams

def load_players_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM player"))
    players = []
    column_names = result.keys()
    for row in result.all(): 
      players.append(dict(zip(column_names, row)))
    return players

def load_locations_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM player"))
    locations = []
    column_names = result.keys()
    for row in result.all(): 
      locations.append(dict(zip(column_names, row)))
    return locations

      
@app.route("/")
def hello_world():
  games = load_games_from_db()
  return render_template('home.html', games=games)

@app.route("/all_stats.html")
def all_stats():
  games = load_games_from_db()
  teams = load_teams_from_db()
  players = load_players_from_db()
  return render_template('all_stats.html', games=games, teams=teams, players=players)

@app.route("/game_stats.html")
def game_stats():
  games = load_games_from_db()
  # Load Filtered Home Team
  query = "SELECT DISTINCT homeTeam FROM game"
  with engine.connect() as conn:
      result = conn.execute(text(query))
      home_teams = [row[0] for row in result]
  # Load Filtered Away Team
  queryAway = "SELECT DISTINCT awayTeam FROM game"
  with engine.connect() as conn:
      result = conn.execute(text(queryAway))
      away_teams = [row[0] for row in result]
  # Load Filtered Team
  queryBoth = "SELECT DISTINCT homeTeam FROM game UNION SELECT DISTINCT awayTeam FROM game"
  with engine.connect() as conn:
      result = conn.execute(text(queryBoth))
      all_teams = [row[0] for row in result]
  # Load Locations
  queryLocation = "SELECT DISTINCT location FROM game"
  with engine.connect() as conn:
      result = conn.execute(text(queryLocation))
      locations = [row[0] for row in result]
  # Load Game Ids
  queryDelete = "SELECT DISTINCT game_id FROM game"
  with engine.connect() as conn:
      result = conn.execute(text(queryDelete))
      gameId = [row[0] for row in result]
  return render_template('game_stats.html', games=games, homeTeams=home_teams, awayTeams=away_teams, allTeams=all_teams, gameId=gameId, locations=locations)

@app.route("/player_stats.html")
def player_stats():
  players = load_players_from_db()
  return render_template('player_stats.html', players=players)

@app.route("/team_stats.html")
def team_stats():
  teams = load_teams_from_db()
  return render_template('team_stats.html', teams=teams)

@app.route("/add_game.html")
def add_game_page():
  games = load_games_from_db()
  return render_template('add_game.html', games=games)

@app.route("/add_team.html")
def add_team_page():
  games = load_games_from_db()
  return render_template('add_team.html', games=games)

@app.route("/add_player.html")
def add_player_page():
  games = load_games_from_db()
  return render_template('add_player.html', games=games)

@app.route("/add_game", methods=["POST"])
def add_game():
  # Retrieve data from the form
  date = request.form.get("date")
  home_team = request.form.get("homeTeam")
  home_city = request.form.get("homeCity")  # Add this line
  away_team = request.form.get("awayTeam")
  away_city = request.form.get("awayCity")  # Add this line
  location = request.form.get("location")
  outcome = request.form.get("outcome")
  
  # Create a new Game instance
  new_game = Game(
      date=date,
      homeTeam=home_team,
      homeCity=home_city,  # Add this line
      awayTeam=away_team,
      awayCity=away_city,  # Add this line
      location=location,
      outcome=outcome,
  )

  # Create a session
  session = Session()

  # Check if the home team exists in the team table
  existing_home_team = session.query(Team).filter_by(name=home_team).first()
  if not existing_home_team:
      # Create a new Team object for the home team
      new_home_team = Team(name=home_team, city=home_city)
      session.add(new_home_team)

  # Check if the away team exists in the team table
  existing_away_team = session.query(Team).filter_by(name=away_team).first()
  if not existing_away_team:
      # Create a new Team object for the away team
      new_away_team = Team(name=away_team, city=away_city)
      session.add(new_away_team)

  try:
    # Add the new game instance to the session
    session.add(new_game)

    # Commit the transaction to save the new game to the database
    session.commit()

    # Redirect the user back to the home page or any other appropriate page
    return redirect("/")
  except Exception as e:
      # Handle any exceptions or errors here
      print(f"Error: {e}")
      session.rollback()
  finally:
      # Close the session
      session.close()

@app.route("/add_team", methods=["POST"])
def add_team():
    # Retrieve data from the form
    name = request.form.get("name")
    city = request.form.get("city")

    # Create a new Team instance
    new_team = Team(
        name=name,
        city=city,
    )

    # Create a session
    session = Session()

    try:
        # Add the new team instance to the session
        session.add(new_team)

        # Commit the transaction to save the new team to the database
        session.commit()

        # Redirect the user back to the home page or any other appropriate page
        return redirect("/")
    except Exception as e:
        # Handle any exceptions or errors here
        print(f"Error: {e}")
        session.rollback()
    finally:
        # Close the session
        session.close()

@app.route("/add_player", methods=["POST"])
def add_player():
    # Retrieve data from the form
    name = request.form.get("name")
    salary = request.form.get("salary")
    team = request.form.get("team")
    team_city = request.form.get("teamCity")

    # Create a new Player instance
    new_player = Player(
        name=name,
        salary=salary,
        team=team,
        teamCity=team_city,
    )

    # Create a session
    session = Session()

    existing_team = session.query(Team).filter_by(name=team, city=team_city).first()
    if not existing_team:
        # Create a new Team object for the player's team
        new_team = Team(name=team, city=team_city)
        session.add(new_team)

    try:
        # Add the new player instance to the session
        session.add(new_player)

        # Commit the transaction to save the new player to the database
        session.commit()

        # Redirect the user back to the home page or any other appropriate page
        return redirect("/")
    except Exception as e:
        # Handle any exceptions or errors here
        print(f"Error: {e}")
        session.rollback()
    finally:
        # Close the session
        session.close()

      
print(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
  