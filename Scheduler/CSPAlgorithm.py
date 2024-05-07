import random
from tools.is_consistent import is_consistent
from tools.updateSchedule import updateSchedule
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, udf
# from pyspark.sql.types import StringType

class CSPAlgorithm:
    def __init__(self, block_course_req_variable, instructors, rooms, day_range, time_range, course_with_IntructorID, room_type) -> None:
        self.block_course_req_variable = block_course_req_variable  #programBlocksInfo, courseCode, roomType, durationNum, schedNum
        self.instructors = instructors # courseCode : list of instructor
        self.rooms = rooms #room info
        self.day_range = day_range
        self.time_range = time_range
        self.course_with_IntructorID = course_with_IntructorID #check teacher who have the specialization of the course
        self.room_type = room_type #check room by room type
        
        self._program = set(programBlocksInfo for programBlocksInfo, _, _, _, _ in self.block_course_req_variable) # get unique program since i get all the course inside the program
        
        self.instructor_handle_course = {}
        self.BlockSchedule = {program: {day: {time: True for time in self.time_range} for day in self.day_range} for program in self._program}
        self.InstructorSchedule = {instructor['_id']: {day: {time: True for time in self.time_range} for day in self.day_range} for instructor in self.instructors}
        self.RoomSchedule = {room['_id']: {day: {time: True for time in self.time_range} for day in self.day_range} for room in self.rooms}
        # print(self.RoomSchedule)
        
        # #spark
        # self.spark = SparkSession.builder.appName("Scheduling").getOrCreate() #spark

    def update_Schedule(self, assignment):
        self.instructor_handle_course = {}
        self.BlockSchedule = {program: {day: {time: True for time in self.time_range} for day in self.day_range} for program in self._program}
        self.InstructorSchedule = {instructor['_id']: {day: {time: True for time in self.time_range} for day in self.day_range} for instructor in self.instructors}
        self.RoomSchedule = {room['_id']: {day: {time: True for time in self.time_range} for day in self.day_range} for room in self.rooms}
        updateSchedule(assignment, self.BlockSchedule, self.InstructorSchedule, self.RoomSchedule, self.instructor_handle_course)
        
    def CSPSolver(self):
        assignment = {}
        result = self.Backtracking(assignment)
        print(result)
        return assignment
    
    def Backtracking(self, assignment):
        #update schedule for their availability
        self.update_Schedule(assignment)
        
        if len(assignment) == len(self.block_course_req_variable):  # All variables assigned for both schedules
            print('scheduling successfully')
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        if var is None:
            return assignment  # All variables are assigned but the assignment is not complete

        for value in self.order_domain_value(var, assignment):
            assignment[var] = value
            if is_consistent(assignment, self.course_with_IntructorID, self.room_type):
                result = self.Backtracking(assignment)
                if result is not None:
                    return result
            else:
                del assignment[var]
                
        return None
        
    def select_unassigned_variable(self, assignment):
        # Find the set of unassigned courses
        unassigned_courses = [course for course in self.block_course_req_variable if course not in assignment]
        # Select the next unassigned course using a heuristic (e.g., MRV)
        if unassigned_courses:
            random.shuffle(unassigned_courses)
            sortToSChed  = sorted(unassigned_courses, key=lambda var: (var[2] != 'Laboratory', var[4] != 1, var[4] != 2, var[0])) #priority sched for laboratory and schedule number 1 
            return sortToSChed[0]  # For simplicity, select the first unassigned course
        else:
            return None  # If all courses are assigned, return None
      
    #spark      
    def order_domain_value(self, variable, assignment):
        # Get the domain values for the course variable
        domain_values = self.get_domain_values(variable, assignment)
        
        # Sort the domain values based on a heuristic or strategy
        sorted_domain_values = sorted(domain_values, key=lambda value: self.heuristic_function(value, variable, assignment), reverse=True)
        
        return sorted_domain_values
    
    def get_domain_values(self, variable, assignment):
        programBlocksInfo, courseCode, _, durationNum, schedNum = variable
        
        invalid_domain_cache = set() #this cache is for checking if the value is is invalid to limit the solving time
        
        domain_values = []
        if schedNum == 1:
            for instructor in self.instructors:
                #check if the instructor reach the limit of course to handle
                if instructor['_id'] in self.instructor_handle_course:
                    if courseCode not in self.instructor_handle_course[instructor['_id']]: 
                        if len(self.instructor_handle_course[instructor['_id']]) + 1 > 5: # do not exceed to maximum of 5 course instructor can handle 
                            continue
                    
                for room in self.rooms:
                    for day in self.day_range:
                        for start_time in range(7, 32 - durationNum):
                            end_time = start_time + durationNum
                            if invalid_domain_cache is not None and self.is_not_in_invalid_domain_cache(invalid_domain_cache, programBlocksInfo, instructor['_id'], room['_id'], day, start_time, end_time):
                                if self.is_valid_pairs(invalid_domain_cache, programBlocksInfo, instructor['_id'], room['_id'], day, start_time, end_time):
                                    domain_values.append((instructor['_id'], room['_id'], day, start_time, end_time)) #  format for value
                                
        if schedNum == 2:
            # getInstructor is for retriving the same instructor from schedule number 1 as a requirements
            getInstructor = next((value[0] for key, value in assignment.items() if key[:2] == (programBlocksInfo, courseCode)), None)
            if getInstructor is None:
                print('there is no assigned schedule number 1 in  ', (programBlocksInfo, courseCode))
                
            instructor = getInstructor
            for room in self.rooms:
                for day in self.day_range:
                    for start_time in range(7, 32 - durationNum):
                        end_time = start_time + durationNum
                        if invalid_domain_cache is not None and self.is_not_in_invalid_domain_cache(invalid_domain_cache, programBlocksInfo, instructor, room['_id'], day, start_time, end_time):
                            if self.is_valid_pairs(invalid_domain_cache, programBlocksInfo, instructor, room['_id'], day, start_time, end_time):
                                domain_values.append((instructor, room['_id'], day, start_time, end_time)) #  format for value
        
        if schedNum == 3:
            # getInstructor is for retriving the same instructor from schedule number 1 and 2 as a requirements
            getInstructor = next((value[0] for key, value in assignment.items() if key[:2] == (programBlocksInfo, courseCode)), None)
            if getInstructor is None:
                print('there is no assigned schedule number 1 or 2 in  ', (programBlocksInfo, courseCode))
                
            instructor = getInstructor
            for day in self.day_range:
                for start_time in range(7, 32 - durationNum):
                    end_time = start_time + durationNum
                        
                    if invalid_domain_cache is not None and self.is_not_in_invalid_domain_cache(invalid_domain_cache, programBlocksInfo, instructor, 'Online', day, start_time, end_time):
                        if self.is_valid_pairs(invalid_domain_cache, programBlocksInfo, instructor, 'Online', day, start_time, end_time):
                            domain_values.append((instructor, 'Online', day, start_time, end_time)) #  format for value
                            
        return domain_values
    
    def is_not_in_invalid_domain_cache(self, invalid_domain_cache, programBlocksInfo, instructor, room, day, start_time, end_time):
        #validation inside invalid cache
        if (programBlocksInfo, day, start_time) in invalid_domain_cache or \
            (programBlocksInfo, day, end_time) in invalid_domain_cache:
                return False
        # if (instructor, day, start_time) in invalid_domain_cache or \
        #     (instructor, day, end_time) in invalid_domain_cache:
        #         return False
        if room != 'Online':
            if (room, day, start_time) in invalid_domain_cache or \
                (room, day, end_time) in invalid_domain_cache:
                    return False    
        return True
    
    def is_valid_pairs(self, invalid_domain_cache, programBlocksInfo, instructor, room, day, start_time, end_time):
        is_valid = True
        
        for ts in range(start_time, end_time):
            if not self.BlockSchedule[programBlocksInfo][day][ts]:
                is_valid = False
                invalid_domain_cache.add((programBlocksInfo, day, ts))
                
            # if not self.InstructorSchedule[instructor][day][ts]:
            #     is_valid = False    
            #     invalid_domain_cache.add((instructor, day, ts))
                
            if room != 'Online':
                if not self.RoomSchedule[room][day][ts]:
                    is_valid = False
                    invalid_domain_cache.add((room, day, ts))

        return is_valid
       
    def heuristic_function(self, value, variable,assignment):
        programBlocksInfo, courseCode, courseRoomType, durationNum, schedNum = variable
        instructor_id, room_id, day, start_time, end_time = value
        
        score = 0
        
        if not self.instructor_consecutive_hrs(instructor_id, day, start_time, end_time, durationNum): #check if the instructor has rest or don't have
            score -= 1
            
        if not self.instructor_hrs_limit(instructor_id, day, durationNum): #check if the instructor daily hours limit is respected
            score -= 1
            
        if not self.blocks_consecutive_hrs(programBlocksInfo, day, start_time, end_time, durationNum): #check if the block have rest or don't have
            score -= 1
            
        if not self.instructor_specialization(instructor_id, courseCode): #check if the course is not specialized by intructor
            score -= 1
            
        if not self.room_type_validation(room_id, courseRoomType): #check if the requirements for course room type is respected
            score -= 1
        
        if schedNum != 1:
            if not self.course_schedule(programBlocksInfo, courseCode, schedNum, day, assignment): #check if the schedule1,2 and if have schedule 3 contains atleast 1 day gap in between 
                score -= 1
                
        if schedNum == 1: # i want to assign different instructor per course 
            if not self.instructor_not_been_scheduled(instructor_id, assignment):
                score -= 1
            
        return score
        
    def instructor_consecutive_hrs(self, instructor_id, day, start_time, end_time, durationNum):
        if instructor_id not in self.InstructorSchedule:
            return True
        if day not in self.InstructorSchedule[instructor_id]:
            return True
        
        consecutive_hours = 0 #count consecutive time 
        
        # Check consecutive hours before the given start time
        for ts in range(start_time - 1, max(start_time - 6, 7) - 1, -1): #-6 to count 3 hours before the assignmnet
            if not self.InstructorSchedule[instructor_id][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        for ts in range(end_time - 1, min(end_time + 6, 31)): # +6 to count 3 hours after the assignmnet
            if not self.InstructorSchedule[instructor_id][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        return (durationNum + consecutive_hours) > 8 #if durationNum + consecutive_hours is less than 8 (4 hours) return true
    
    def instructor_hrs_limit(self, instructor_id, day, durationNum):
        if instructor_id not in self.InstructorSchedule:
            return True
        if day not in self.InstructorSchedule[instructor_id]:
            return True
        
        # Get the schedule for the specified instructor and day
        schedule = self.InstructorSchedule.get(instructor_id, {}).get(day, {})
        # Count the number of False values
        count_false = sum(1 for time_slot in schedule.values() if not time_slot)
        
        return (count_false + durationNum) > 12 #if num of false with number of duration to be occupied is less than 12 (6 hours) return true
    
    def blocks_consecutive_hrs(self, programBlocksInfo, day, start_time, end_time, durationNum):
        if programBlocksInfo not in self.BlockSchedule:
            return True
        if day not in self.BlockSchedule[programBlocksInfo]:
            return True
        
        consecutive_hours = 0 #count consecutive time 
        
        # Check consecutive hours before the given start time
        for ts in range(start_time - 1, max(start_time - 6, 7) - 1, -1): #-6 to count 3 hours before the assignmnet
            if not self.BlockSchedule[programBlocksInfo][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        for ts in range(end_time - 1, min(end_time + 6, 31)): # +6 to count 3 hours after the assignmnet
            if not self.BlockSchedule[programBlocksInfo][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        return (durationNum + consecutive_hours) > 8 #if durationNum + consecutive_hours is less than 8 (4 hours) return true
    
    def instructor_specialization(self, instructor_id, courseCode):
        if instructor_id not in self.course_with_IntructorID[courseCode]:
            return False
        return True
    
    def room_type_validation(self, room_id, courseRoomType):
        if room_id not in self.room_type[courseRoomType]:
            return False
        return True
    
    def course_schedule(self, programBlocksInfo, courseCode, schedNum, day, assignment):
        matching_schedules = [(key, value) for key, value in assignment.items() if key[:2] == (programBlocksInfo, courseCode)]
        
        sched_number_to_validate = schedNum - 1 # get schedule number 1 if i need to validate schedule number 2 and get schedule number 2 if i need to validate the schedule number 3 
        
        # assigned_day_schedule is to get the assign value of day from the schedule number to be validate the current value
        assigned_day_schedule = next((value[2] for key, value in matching_schedules if key[-1] == sched_number_to_validate), None)
        
        if assigned_day_schedule is not None and day - assigned_day_schedule <= 1: # this where i validate if the schedule have 1 day or more gap between the last schedule and current schedule
            return False

        return True
            
    def instructor_not_been_scheduled(self, instructor_id, assignment):
        matching_schedules = [value for value in assignment.values() if value[0] == instructor_id] #filterd with the same instructor_id

        if matching_schedules:
            return False
        
        return True
    
    
    