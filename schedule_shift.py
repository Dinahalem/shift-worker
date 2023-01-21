#Create a list of workers
workers = ['John', 'Paul', 'George', 'Ringo']

#Create a list of shifts 
shifts = ['0-8', '8-16', '16-24']

#Create an empty dictionary to store the schedule 
schedule = {} 

#Loop through the workers and assign each worker a shift for each day 
for worker in workers: 

    #Set the day counter to 0 
    day = 0

    #Loop through the shifts and assign one shift per day for each worker 
    for shift in shifts:

        #Assign each worker a shift for that day and increment the day counter by 1 
        schedule[(worker,day)] = shift 
        day += 1  

        #Check if we have reached the end of the week (7 days) and reset the counter if we have 
        if day == 7:  

            #Reset the counter to 0 so that we start again from Monday  
            day = 0  

            #Loop through all workers again starting from the next one in line  
            break  

    #Print out our final schedule    																    
    print(schedule)
