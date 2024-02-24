# import function from __init__.py
from website import create_app

app=create_app()

# only if we run this file we will run the web server
if __name__ == '__main__':

    app.run(debug=True)
