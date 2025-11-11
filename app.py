from src import create_app
from config import DEBUG
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)