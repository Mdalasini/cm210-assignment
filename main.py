from internals.api.api import app
from internals.db.connection import init_connection

if __name__ == '__main__':
  init_connection("database/library.db")
  app.run(debug=True)