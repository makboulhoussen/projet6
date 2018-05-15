#! /usr/bin/env python
import tags.api
from tags.api import app

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

