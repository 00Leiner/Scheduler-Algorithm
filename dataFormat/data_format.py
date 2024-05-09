def formatting_data(result, course_details, teacher_details, room_details):
    if result is None:
        print('result is None')
        return
    
    formatted = {
        'programs': []
    }
    
    for key, value in result.items():
        (program, major, year, semester, block) = key[0]
        course_code = key[1]
        schedNum = key[4]
        instructor = value[0]
        room = value[1]
        day = value[2]
        start_time = value[3]
        end_time = value[4]
        
        courseCode = course_details[course_code]['code']
        courseDescription = course_details[course_code]['description']
        courseUnit = course_details[course_code]['units']
        fname = teacher_details[instructor]['fname']
        sname = teacher_details[instructor]['sname']
        roomName = room_details[room]['name'] if room != 'Online' else 'Online'
        
        # Find or create the program entry in formatted_data
        program_entry = next((prog for prog in formatted['programs'] if prog['program'] == program and prog['major'] == major and prog['year'] == year and prog['semester'] == semester and prog['block'] == block), None)
        if program_entry is None:
            program_entry = {
                'program': program,
                'major': major,
                'year': year,
                'semester': semester,
                'block': block,
                'sched': []
            }
            formatted['programs'].append(program_entry)
        
        # Find or create the course entry in program_entry['sched']
        course_entry = next((course for course in program_entry['sched'] if course['courseCode'] == course_code), None)
        if course_entry is None:
            course_entry = {
                'courseCode': courseCode,
                'courseDescription': courseDescription,
                'courseUnit': courseUnit,
                'instructor': f'{fname} {sname}',
                'schedule': []
            }
            program_entry['sched'].append(course_entry)
        
        # Append the schedule details to course_entry['sched']
        schedule_details = {
            'schedNum': schedNum,
            'room': roomName,
            'day': get_day_name(day),
            'startTime': format_time(start_time),
            'endTime': format_time(end_time)
        }
        course_entry['schedule'].append(schedule_details)
    
    return formatted


def get_day_name(day):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Ensure that the day value is a string representing a number
    try:
        day_number = int(day)
        if 1 <= day_number <= 5:
            return days_of_week[day_number - 1]
        else:
            return "Invalid Day"
    except ValueError:
        return "Invalid Day"
    
def format_time(time):
  hour = 7 + (time - 7) // 2  # Calculate the hour component
  minute = "30" if time % 2 == 0 else "00"  # Determine the minute component (either "00" or "30")
  am_pm = "AM" if hour < 12 else "PM"  # Determine if it's AM or PM
  hour = hour if hour <= 12 else hour - 12  # Convert to 12-hour format
  return f"{hour}:{minute} {am_pm}"