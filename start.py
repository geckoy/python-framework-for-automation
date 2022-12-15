from App.Helpers import *

if "__main__" == __name__ :
    try: 
        isdebug = sys.argv[1];isdebug = True if isdebug == "True" else False 
    except: raise undefinedArgs("Please specify the debug mode")
    app = getApplication(False, debug=isdebug)
    app.initiate()