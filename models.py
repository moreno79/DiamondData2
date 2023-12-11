from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
  __tablename__ = 'game'

  game_id = Column(Integer, primary_key=True)
  date = Column(Date, nullable=False)
  homeTeam = Column(String(255), nullable=False)
  homeCity = Column(String(255), nullable=False)  # Add this line
  awayTeam = Column(String(255), nullable=False)
  awayCity = Column(String(255), nullable=False)  # Add this line
  location = Column(String(255), nullable=False)
  outcome = Column(String(255), nullable=False)

class Team(Base):
  __tablename__ = 'team'

  team_id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  city = Column(String(255), nullable=False)

  def __init__(self, name, city):
      self.name = name
      self.city = city

class Player(Base):
  __tablename__ = 'player'

  player_id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  salary = Column(Float, nullable=False)
  team = Column(String(255), nullable=False)
  teamCity = Column(String(255), nullable=False)

  def __init__(self, name, salary, team, teamCity):
      self.name = name
      self.salary = salary
      self.team = team
      self.teamCity = teamCity
