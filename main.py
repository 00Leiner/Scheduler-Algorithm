import requests
from flask import Flask, jsonify
from getData.student_data import fetch_student_data
from getData.room_data import fetch_room_data
from getData.teacher_data import fetch_teacher_data
from getData.course_data import fetch_course_data
from getData.curriculum_data import fetch_curriculum_data
from Scheduler.CSPAlgorithm import CSPAlgorithm
from variable_format.block_course_variable import block_course_variable
from variable_format.course_with_teacherID import instructor_specialization
from variable_format.room_type import room_info

class Scheduler:
    def __init__(self) -> None:
        self.getData()
    
    def getData(self):
        ip = '192.168.1.6'
        self.block_course_req_variable = block_course_variable(fetch_student_data(ip), fetch_curriculum_data(ip)) #program, major, year, block, courseCode, roomType, durationNum, schedNum
        self.instructors = fetch_teacher_data(ip) # courseCode : list of instructor
        self.rooms = [room for room in fetch_room_data(ip)] # room info
        self.day_range = range(1, 6) # Mon - Friday
        self.time_range = range(7, 32) #7am - 7pm
        self.course_with_IntructorID = instructor_specialization(fetch_course_data(ip), self.instructors) #for instructor specialization validation
        self.room_type = room_info(self.rooms) #for room type validation
        # print(len(self.room_type))
        
    def CSP(self):
        csp = CSPAlgorithm(self.block_course_req_variable, self.instructors, self.rooms, self.day_range, self.time_range, self.course_with_IntructorID, self.room_type)
        csp.CSPSolver()
        
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000)
    scheduler = Scheduler()
    s = scheduler.CSP()
    # print(s)