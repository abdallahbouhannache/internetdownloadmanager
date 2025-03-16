THINGS TO FIX 






1-Research async vs threads vs eventlet in Socket.IO
2-Set file_lock as new/singleton per event loop
3-Set status_lock as singleton across all event loops
4-Read file status at endpoint call start
5-Check local file size for download amount
6-Append downloaded parts in correct order
7-Ensure chunk write order doesn’t affect file
8-Improve observer vs main app with tasks
9-Create tests




MAKE READING THE FILE STATUS AT START OF ENDPOINT CALL 
CHECK THE SIZE OF LOCAL FILE EXISTING SO I CAN DEFINE HOW MUCH I AM REQUIRED TO DOWNLOAD 
MAKE SURE 

    # this should be new/singleton over each new event loop
    file_lock
    # this should be singleton over all the events loops  ,
    status_lock

    make sure downloaded parts are appended in the right order
    make sure that the order of writing the chunks does not affect the file downloaded file
    
    check diffrence between async and threads and event and eventlet in socketsIO
    
    


    UNDERSTAND HOW TO IMPROVE OBSERVER VS THE main app that runs with tasks

    create tests
********
    LEARN HOW TO USE TEST DRIVEN DEV IN NEXT PROJECT (MEDICAL MANAGEMENT APP)