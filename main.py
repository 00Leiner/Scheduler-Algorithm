import requests
from flask import Flask, jsonify
from dataFormat.data_format import formatting_data
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
        self.courses = fetch_course_data(ip)
        # print(len(self.room_type))
        
    def CSP(self):
        csp = CSPAlgorithm(self.block_course_req_variable, self.instructors, self.rooms, self.day_range, self.time_range, self.course_with_IntructorID, self.room_type)
        result = csp.CSPSolver()
        return result
    
    def formatting(self):
        course_details = {course['code']: course for course in self.courses}
        teacher_details = {teacher['_id']: teacher for teacher in self.instructors}
        room_details = {room['_id']: room for room in self.rooms}
        result = self.CSP()
        formatted = formatting_data(result, course_details, teacher_details, room_details)
        return formatted
    
app = Flask(__name__)
class Fetching:
    def __init__(self):
        self.url = 'http://192.168.1.6:3000/Schedule/create'

    def perform_post_request(self, data):
        response = requests.post(self.url, json=data)

        if response.status_code in [200, 201]:
            return response
        else:
            print(f"Error in POST request. Status code: {response.status_code}")
            print(response.text)
            return response

@app.route('/activate_csp_algorithm', methods=['POST'])
def activate_csp_algorithm():
    try:
        scheduler = Scheduler()
        result = scheduler.formatting()
        
        fetching_instance = Fetching()
        response = fetching_instance.perform_post_request(result)
        print(response.text)
  
        return jsonify({"status": "success", "message": "CSP algorithm activated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
        
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000)
    scheduler = Scheduler()
    s = scheduler.formatting()
    print(s)
    
    