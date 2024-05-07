def updateSchedule(assignment, BlockSchedule, InstructorSchedule, RoomSchedule, instructor_handle_course):
    if assignment is None:
        return
    
    for var, value in assignment.items():
        (programBlocksInfo, courseCode, _, _, _) = var
        (instructor, room, day, start_time, end_time) = value
        
        # updating instructor handled course
        if instructor not in instructor_handle_course:
            instructor_handle_course[instructor] = set()
        instructor_handle_course[instructor].add(courseCode)
        
        # updating instructor, room, and blocks schedule
        for time_slot in range(start_time, end_time):
            BlockSchedule[programBlocksInfo][day][time_slot] = False
            InstructorSchedule[instructor][day][time_slot] = False
            if room != 'Online':
                RoomSchedule[room][day][time_slot] = False
        