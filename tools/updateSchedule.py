def updateSchedule(assignment, BlockSchedule, InstructorSchedule, RoomSchedule):
    if assignment is None:
        return
    
    for var, value in assignment.items():
        (program,_, _, durationReq, _) = var
        (day, time_start, room, instructor) = value
        
        for time_slot in range(time_start, time_start + durationReq):
            BlockSchedule[program][day][time_slot] = False
            InstructorSchedule[room][day][time_slot] = False
            RoomSchedule[instructor][day][time_slot] = False
        