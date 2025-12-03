# convenience script to run the triangulator server
from TP.triangulator.server import app

if __name__ == "__main__":
    app.run(port=5000)
