def is_consistent(assignmnet, course_with_IntructorID, room_type):
    print()
    print('=======================================================================')
    
    is_valid = True # check if the assignmnet is valid to return
    
    instructo_max_course = {} #making sure only 5 course can teacher been assigned
    
    # for validating no overlapping schedule
    instructor_schedule = {} 
    blocks_schedule = {}
    room_schedule = {}
    
    check_same_block_course = set() # check if blocks and course is repeatedly assigned
    
    #key = programBlocksInfo, courseCode, roomType, durationNum, schedNum
    #value = instructor_id, room_id, day, start_time, end_time
    for key, value in assignmnet.items(): 
        
        #check duplicate
        if key not in check_same_block_course:
            check_same_block_course.add(key)
        else:
            is_valid = False
        
        for key2, value2 in assignmnet.items():
            
            if key[:2] == key2[:2]: # same blocks, course
                
                #check if the same blocks and course has the same instructor 
                if value[0] != value2[0]:
                    is_valid = False
            
                #check schedule 1,2, and 3 is not in the same day
                if key[4] != key2[4] and value[2] == value2[2]:
                    is_valid = False
          
        # check possible time conflict
        if value[0] in instructor_schedule: #instructor
            if value[2] in instructor_schedule[value[0]]:
                for ts in range(value[3], value[4]):
                    if ts in instructor_schedule[value[0]][value[2]]:
                        is_valid = False
                    else:
                        print('time conflict with instructor: ', value[0], 'day: ', value[2], 'time: ', ts)
        
        if key[0] in blocks_schedule: #block
            if value[2] in blocks_schedule[key[0]]:
                for ts in range(value[3], value[4]):
                    if ts in blocks_schedule[key[0]][value[2]]:
                        is_valid = False
                    else:
                        print('time conflict with program block: ', key[0], 'day: ', value[2], 'time: ', ts)
                        
        if value[1] in room_schedule: #room
            if value[2] in room_schedule[value[1]]:
                for ts in range(value[3], value[4]):
                    if ts in room_schedule[value[1]][value[2]]:
                        is_valid = False
                    else:
                        print('time conflict with room: ',value[1], 'day: ', value[2], 'time: ', ts)
                        
        add_value_in_schedule(key, value, instructor_schedule, blocks_schedule, room_schedule) #update schedule
        
        # check instructor specialization
        if value[0] not in course_with_IntructorID[key[1]]:
            print('instructor: ', value[0], 'is forced assigned to: ', key[1])
        
        # check instructor and blocks if have rest and no rest
        
        # course type for room type. check if the course required type is fallowed
        if value[1] not in room_type[key[2]]:
            print('the course: ', key[1], ' schedule number: ', key[4], ' is schedule in: ', value[1])
        
        
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
        if blocks_consecutive_hours + key[3] > 8:
            print("block: ", key[0], " have consecutive time of: ", blocks_consecutive_hours, ' in day: ', value[2])
        if instructor_consecutive_hours + key[3] > 8:
            print("block: ", value[0], " have consecutive time of: ", instructor_consecutive_hours, ' in day: ', value[2])
        
        if len(instructor_schedule[value[0]][value[2]]) > 6:
            print('instructor: ', value[0], ' is scheduled: ', len(instructor_schedule[value[0]][value[2]]),'hrs', ' in day of: ', value[2])
        
    print()
    return is_valid
        
        
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
    if value[1] not in room_schedule:
        room_schedule[value[1]] = {}
    if value[2] not in room_schedule[key[0]]:
        room_schedule[value[1]][value[2]] = set()
        
    # add ts in block, instructor, room schedule
    for ts in range(value[3], value[4]):
        instructor_schedule[value[0]][value[2]].add(ts)
        blocks_schedule[key[0]][value[2]].add(ts)
        room_schedule[value[1]][value[2]].add(ts)