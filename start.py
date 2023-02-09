from App.Helpers import *

if "__main__" == __name__ :
    try: 
        isdebug = sys.argv[1];isdebug = True if isdebug == "True" else False 
    except: raise undefinedArgs("Please specify the debug mode")
    try:
        sepcific_processes = sys.argv[2]
    except:
        sepcific_processes = ""
    app = getApplication(False, debug=isdebug, specific_processes=sepcific_processes)
    app.initiate()