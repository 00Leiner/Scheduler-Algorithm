from comments.comments import overlap_comments, no_rest, force_assignmnet, vacant, exceeding_max_course

def getComments(result, course_with_IntructorID, room_type):
    comments = []
    
    instructo_max_course = {} # making sure only 5 course can teacher been assigned
    
    # for validating no overlapping schedule
    instructor_schedule = {} 
    blocks_schedule = {}
    room_schedule = {}
    
    #key = programBlocksInfo, courseCode, roomType, durationNum, schedNum
    #value = instructor_id, room_id, day, start_time, end_time
    for key, value in result.items(): 
        
        # check possible time conflict
        if value[0] in instructor_schedule: #instructor
            if value[2] in instructor_schedule[value[0]]:
                for ts in range(value[3], value[4]):
                    if ts in instructor_schedule[value[0]][value[2]]:
                        print('time conflict with instructor: ', value[0], 'day: ', value[2], 'time: ', ts)
                        
        if key[0] in blocks_schedule: #block
            if value[2] in blocks_schedule[key[0]]:
                for ts in range(value[3], value[4]):
                    if ts in blocks_schedule[key[0]][value[2]]:
                        print('time conflict with program block: ', key[0], 'day: ', value[2], 'time: ', ts)
                        
        if value[1] != 'Online': #check if not online
            if value[1] in room_schedule: #room
                if value[2] in room_schedule[value[1]]:
                    for ts in range(value[3], value[4]):
                        if ts in room_schedule[value[1]][value[2]]:
                            print('time conflict with room: ',value[1], 'day: ', value[2], 'time: ', ts)
                            
        add_value_in_schedule(key, value, instructor_schedule, blocks_schedule, room_schedule) #update schedule
        
        # check instructor specialization
        if value[0] not in course_with_IntructorID[key[1]]:
            print('instructor: ', value[0], 'is forced assigned to: ', key[1])
        
        # course type for room type. check if the course required type is fallowed
        if value[1] not in room_type[key[2]]:
            print('the course: ', key[1], ' schedule number: ', key[4], ' is schedule in: ', value[1])
        
        # check instructor and blocks if have rest and no rest
        # Initialize consecutive hours counter
        blocks_consecutive_hours = 0
        instructor_consecutive_hours = 0
        
        # Check consecutive hours before the given start time for instructor and blocks
        for ts in range(value[3] - 1, max(value[3] - 6, 7) - 1, -1):
            if ts in instructor_schedule[value[0]][value[2]]:
                instructor_consecutive_hours += 1
            else: break
        for ts in range(value[3] - 1, max(value[3] - 6, 7) - 1, -1):
            if ts in blocks_schedule[key[0]][value[2]]:
                blocks_consecutive_hours += 1
            else: break
            
        # Check consecutive hours after the given end time for instructor and blocks
        for ts in range(value[4] - 1, min(value[4] + 6, 31)):
            if ts in instructor_schedule[value[0]][value[2]]:
                instructor_consecutive_hours += 1
            else: break
            
        for ts in range(value[4] - 1, min(value[4] + 6, 31)):
            if ts in blocks_schedule[key[0]][value[2]]:
                blocks_consecutive_hours += 1
            else: break
            
        # Check if more than 4 hours of consecutive hours are scheduled within the day for instructor AND BLOCKS
        if (blocks_consecutive_hours + key[3]) > 8:
            print("block: ", key[0], " have consecutive time of: ", blocks_consecutive_hours,'hrs', ' in day: ', value[2])
           
        if (instructor_consecutive_hours + key[3]) > 8:
            print("block: ", value[0], " have consecutive time of: ", instructor_consecutive_hours,'hrs', ' in day: ', value[2])
        
        #check the limit of instructor with maximum hours a day 
        if len(instructor_schedule[value[0]][value[2]]) > 12:
            print('instructor: ', value[0], ' is scheduled: ', len(instructor_schedule[value[0]][value[2]]) / 2,'hrs', ' in day of: ', value[2])
        
        #check maximum of courses can instructor handle
        if value[0] not in instructo_max_course:
            instructo_max_course[value[0]] = set()
        if key[1] not in instructo_max_course[value[0]]:
            if len(instructo_max_course[value[0]]) + 1 > 5:
                print(f"{value[0]} exceeds the maximum courses requirements per Instructor")
                return False
            else: instructo_max_course[value[0]].add(key[1])
       
def add_value_in_schedule(key, value, instructor_schedule, blocks_schedule, room_schedule):
    
    # add value in instructor_schedule
    if value[0] not in instructor_schedule:
            instructor_schedule[value[0]] = {}
    if value[2] not in instructor_schedule[value[0]]:
            instructor_schedule[value[0]][value[2]] = set()
            
    # add value in blocks_schedule
    if key[0] not in blocks_schedule:
        blocks_schedule[key[0]] = {}
    if value[2] not in blocks_schedule[key[0]]:
        blocks_schedule[key[0]][value[2]] = set()
        
    # add value in room_schedule
    if value[1] != 'Online':
        if value[1] not in room_schedule:
            room_schedule[value[1]] = {}
        if value[2] not in room_schedule[value[1]]:
            room_schedule[value[1]][value[2]] = set()
        
    # add ts in block, instructor, room schedule
    for ts in range(value[3], value[4]):
        instructor_schedule[value[0]][value[2]].add(ts)
        blocks_schedule[key[0]][value[2]].add(ts)
        if value[1] != 'Online':
            room_schedule[value[1]][value[2]].add(ts)
        
 