from src.api import app

from src.api.calls import create_user, get_user
from src.api.errors import errors
from src.api.hello_world import hello_world


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
