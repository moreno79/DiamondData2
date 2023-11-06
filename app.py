from flask import Flask, render_template, request, redirect
from database import engine
from sqlalchemy import text

app = Flask(__name__)

def load_data_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM game"))
    games = []
    column_names = result.keys()
    for row in result.all(): 
      games.append(dict(zip(column_names, row)))
    return games



@app.route("/")
def hello_world():
  games = load_data_from_db()
  return render_template('home.html', games=games)

@app.route("/add_game", methods=["POST"])
def add_game():
    # Retrieve data from the form
  # Retrieve data from the form
  date = request.form.get("date")
  home_team = request.form.get("homeTeam")
  away_team = request.form.get("awayTeam")
  location = request.form.get("location")
  outcome = request.form.get("outcome")

  # Create a dictionary to store the parameters
  params = {
      'date': date,
      'homeTeam': home_team,
      'awayTeam': away_team,
      'location': location,
      'outcome': outcome
  }

  # Print the data to check the formatting
  print(f"Date: {params['date']}")
  print(f"Home Team: {params['homeTeam']}")
  print(f"Away Team: {params['awayTeam']}")
  print(f"Location: {params['location']}")
  print(f"Outcome: {params['outcome']}")

  # Create an SQL INSERT statement
  insert_statement = text("INSERT INTO game (date, homeTeam, awayTeam, location, outcome) "
                          "VALUES (:date, :homeTeam, :awayTeam, :location, :outcome)")

  # Execute the SQL INSERT statement using the database engine
  with engine.connect() as conn:
    conn.execute(insert_statement, parameters=params)

  # Redirect the user back to the home page or any other appropriate page
  return redirect("/")

print(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
  