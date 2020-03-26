from GameLife import GameRunner, Application
import numpy as np

if __name__ == "__main__":
  runner = GameRunner()
  app = Application(runner)
  app.run()