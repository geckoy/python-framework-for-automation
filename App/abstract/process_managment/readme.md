This folder serve the abstract concept for the execution of processes which gives the ability to manage them "start, stop, pause, play, ...etc", or running them in synchronous or parallel mode and also virtual or base file execution.

### How it works
the main class is the BaseProcesses, this class is an abstract class which holds the managing and registering of the processes, forces its child classes to define some attributes: 
- *processname* abstract attr which is the category name  of these processes.
- *processespath* abstract attr which holds the path of the intended file processes to run, NOTE: for virtual processes this directory will hold only single file.
- *processesManagerPath* abstract attr this holds the path of the manager class "extends *BaseMultiProcess*" of these processes because each process will be pushed inside this class that will control him like pausing, starting, playing, stopping.
the BaseProcesses class is bag for its processes and as you've seen above we've mentioned virtual processes, its just fancy word that define if this processes will be played base on files or on some data that get pulled from db or from something out of my imagination cause sometimes you need to use same file but multiple times with different data will go though the explanation of this one later "we'll explain each Base class inside process_managment folder then we try to understand them as whole".

The second class is the *BaseMultiProcess* class this one is an abstract class that contain the methods needed to manage the process because each process is pushed as raw class inside the *BaseMultiProcess* and this latter will instantiate it and be its manager for pausing, starting, playing, stopping and also logging success and errors messages in the logs.

the third class is the BaseProcess class this one is an abstract class that forces each process to hold specific attr and methods feel free to check it and get basic understanding about this BaseProcess class. 

now after introducing each Base class we'll make the magic happen, for me personnally i like to explain using examples, we'll be taking two examples one as sync BaseProcesses and the other will be virtual BaseProcesses, let's get in to it:

for now let grap real programming example, we have a simple python app | bot that run as loop and inside this loop we'll be having dispatched events like this: 

	while True:
            try:
                self.eventsApi.app_loop_before()
                self.eventsApi.app_loop_process()
                self.eventsApi.app_loop_after()
            except KeyboardInterrupt:
                break
            except BaseException as err:
                continue
as you see we have three events *loop_before*, *loop_after* and *loop_process*,  now we need to execute some services in some sepcific events to manage our app | bot, to do this we'll use the process_managment concept to handle this problem first of all we need to pick category name for our processes as for now its services so we'll create directory services inside this directory we need to have two main folders 'general' and 'service', the general folder we'll contain the classes that control the services inside the service folder.
general folder will have servicesManager class that extends BaseProcesses class and the purpose of it is to fetch every service class inside the service folder 'this will happen auto' :

	from App.abstract.process_managment.BaseProcesses import BaseProcesses 
	class servicesManager(BaseProcesses):
             processname = "service"
             processespath = "services/service"
             processesManagerPath = "services/general/service"
    
            def __init__(self) -> None:
                  super().__init__()


####  EXAMPLE #1 BaseProcesses using sync mode
__________________________

## This readme need to be finished !