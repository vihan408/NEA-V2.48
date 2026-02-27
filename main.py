import flet
import os
from dotenv import load_dotenv
load_dotenv()
from leaderboards import main


if __name__ == "__main__":
    appMode = os.getenv("appMode", "desktop")
    if appMode == "web":
          flet.app(
              target=main,
              view=flet.AppView.WEB_BROWSER,
              host="0.0.0.0",
              port=int(os.getenv("PORT", 8080))
          )
    else:
        flet.app(target=main)