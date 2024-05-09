def overlap_comments(data_information, day, other_information):
    return f"The {data_information} contains overlapping events on {day}.\nOther information:\n\t{other_information}"

def no_rest(data_information, day, other_information):
    return f"The {data_information} has no rest on {day}.\nOther information:\n\t{other_information}"

def force_assignmnet(data_information, course_code, other_information):
    return f"The {data_information} was Imposed assigned to {course_code}.\nOther information:\n\t{other_information}"
    
def vacant(room, day, time):
    return f"The {room} is vacant on {day} in {time}."

def exceeding_max_course(data_information, courses):
    return f"The {data_information} exceeds the maximum courses requirements per Instructor.\nCourses:\n\t{courses}"