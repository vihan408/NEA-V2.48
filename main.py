import flet
import os
from dotenv import load_dotenv
load_dotenv()
from leaderboards import main
# This will import all of the libraries that will be used in the solution. This is neccessary for creating the GUI via flet, connecting and talking to my database via psycopg2 and using os and dotenv to load and use the credentials(allows me to connect to my database) to my database as well as the keyword for my login system.
# It also imports the neccessary functions from the leaderboards file that is passed into flet.app which makes the GUI
if __name__ == "__main__":
    # This defines whether the solution is hosted as a page in browser or a desktop app
    appMode = os.getenv("appMode", "desktop")
    if appMode == "web":
          flet.app(
              target=main,
              view=flet.AppView.WEB_BROWSER,
              #defines what to type into the browser to access the page
              host="0.0.0.0",
              # Defines that in order to connect you should use either the port specified in the dotenv file, but if a port was not specified there then just default to 8080 instead.
              port=int(os.getenv("PORT", 8080))
          )
    else:
        # Creates the GUI
        flet.app(target=main)
