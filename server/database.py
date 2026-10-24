from sqlmodel import SQLModel, Field, create_engine, Session
from models import Scenario #So the SQLModel knows about the scenario Table

#Creating the Database Engine(starting with local SQLite)....this is like a door to the database
#this tells python to create a  file called finsight_test.db and connect it
DATABASE_URL = "sqlite:///finsight.db"

# echo=True prints the SQL statements to the terminal so you can see them live 
engine = create_engine(DATABASE_URL, echo=True)

#Creating the database table(Migration/Creation)
def init_db():
    #so the class that was created(Scenario), SQLModel registered that table in an 
    #internal registry called metadata...
    #then create_all() scans that registry and builds the actual table in SQLite.
    SQLModel.metadata.create_all(engine)
    #This will create the table 'scenario' in the finsight_test.db file.

def get_session():
    #this opens a temporary connection to the database.
    #with statement opens the database
    with Session(engine) as session:
        # yield acts as a return, but it pauses the session, lets FASTAPU save or fetch data
        # when the API call finishes, python resumes right after the yield.
        # after which with guarantees the connection is safely closed
        yield session
