def instructor_specialization(courses, instructors):
    by_specialization = {}
    for course in courses:
        by_specialization[course['code']] = set()
        for instructor in instructors:
            for specialized in instructor['specialized']:
                if course['code'] == specialized['code']:
                    by_specialization[course['code']].add(instructor['_id'])
                    
    return by_specialization