def updateSchedule(assignment, BlockSchedule, InstructorSchedule, RoomSchedule, instructor_handle_course):
    if assignment is None:
        return
    
    for var, value in assignment.items():
        (programBlocksInfo, courseCode, roomType, durationNum, schedNum) = var
        (day, time_start, room, instructor) = value
        
        # updating instructor handled course
        if instructor not in instructor_handle_course:
            instructor_handle_course[instructor] = set()
        instructor_handle_course[instructor].append(courseCode)
        
        # updating instructor, room, and blocks schedule
        for time_slot in range(time_start, time_start + durationNum):
            BlockSchedule[programBlocksInfo][day][time_slot] = False
            InstructorSchedule[room][day][time_slot] = False
            RoomSchedule[instructor][day][time_slot] = False
        