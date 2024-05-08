def printBlocksScehdule(assignment):
    if assignment is None:
        print("Assignment has None value")
        return
    
    formatted_data = {}
    
    for key, value in assignment.items():
        (program, major, year, semester, block) = key[0]
        course_code = key[1]
        schedNum = key[4]
        instructor = value[0]
        room = value[1]
        day = value[2]
        start_time = value[3]
        end_time = value[4]
        
        # Create or update the formatted_data entry for the program, major, year, semester, block combination
        if (program, major, year, semester, block) not in formatted_data:
            formatted_data[(program, major, year, semester, block)] = {}
        
        if day not in formatted_data[(program, major, year, semester, block)]:
            formatted_data[(program, major, year, semester, block)][day] = []
        
        formatted_data[(program, major, year, semester, block)][day].append((start_time, end_time))
    
    print(len(formatted_data), " Blocks")
    print(formatted_data)


def printInstructorScehdule(assignment):
    if assignment is None:
        print("Assignment has None value")
        return
    
    formatted_data = {}
    
    for key, value in assignment.items():
        (program, major, year, semester, block) = key[0]
        course_code = key[1]
        schedNum = key[4]
        instructor = value[0]
        room = value[1]
        day = value[2]
        start_time = value[3]
        end_time = value[4]
        
        # Create or update the formatted_data entry for the instructor
        if instructor not in formatted_data:
            formatted_data[instructor] = {}
        if day not in formatted_data[instructor]:
            formatted_data[instructor][day] = []
        formatted_data[instructor][day].append((start_time, end_time))
    
    print(len(formatted_data), " Instructor")
    print(formatted_data)

def printRoomScehdule(assignment):
    if assignment is None:
        print("Assignment has None value")
        return
    
    formatted_data = {}
    
    for key, value in assignment.items():
        (program, major, year, semester, block) = key[0]
        course_code = key[1]
        schedNum = key[4]
        instructor = value[0]
        room = value[1]
        day = value[2]
        start_time = value[3]
        end_time = value[4]
        
        # Create or update the formatted_data entry for the instructor
        if room not in formatted_data:
            formatted_data[room] = {}
        if day not in formatted_data[room]:
            formatted_data[room][day] = []
        formatted_data[room][day].append((start_time, end_time))
    
    print(len(formatted_data) - 1, " room") # minus 1 for online class
    print(formatted_data)