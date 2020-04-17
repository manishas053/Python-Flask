#from ideaboard import create_app
from ideaboard import app

#app = create_app()       # creates flask instance

if __name__ == '__main__':      # to run the source file as main pgm, assign name as main, to run an imported module, name = module
    app.run(debug=True)               # run method runs the application , flask application starts by calling run method