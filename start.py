from App.Helpers import *

if "__main__" == __name__ :
    try: 
        isdebug = sys.argv[1];isdebug = True if isdebug == "True" else False 
    except: raise undefinedArgs("Please specify the debug mode")
    a = {}
    for arg in sys.argv[3:]: s=arg.split("=");a[s[0]]=s[1]
    app = getApplication(False, debug=isdebug, supervisor=sys.argv[2], **a)
    app.initiate()