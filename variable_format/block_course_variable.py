def block_course_variable(program_blocks, curriculum):
    _program_curriculum = [] #programBlocksInfo, courseCode, roomType, durationNum, schedNum
    indexed_curriculum = {}
    for curriculum in curriculum:
            key = (curriculum['program'], curriculum['major'], curriculum['year'], curriculum['semester'])
            indexed_curriculum.setdefault(key, []).extend(curriculum['curriculum'])

    for student in program_blocks:
        key = (student['program'], student['major'], student['year'], student['semester'])
        for numBlock in range(int(student['block'])):
            alphabetical_char = chr(65 + numBlock)
            for course in indexed_curriculum.get(key, []):
                if course['type'] == 'Laboratory':
                    _program_curriculum.append(( 
                        (student['program'], 
                        student['major'], 
                        student['year'],
                        student['semester'],
                        alphabetical_char), 
                        course['code'], 
                        'Laboratory',
                        4, # equivalent of 2 hours with 30mins
                        1))
                    
                    _program_curriculum.append((
                        (student['program'], 
                        student['major'], 
                        student['year'], 
                        student['semester'],
                        alphabetical_char), 
                        course['code'], 
                        'Laboratory',
                        4, # equivalent of 2 
                        2))
                    _program_curriculum.append((
                        (student['program'], 
                        student['major'], 
                        student['year'], 
                        student['semester'],
                        alphabetical_char), 
                        course['code'], 
                        'Lecture',
                        2, # equivalent of 1
                        3))
                else:
                    _program_curriculum.append((
                        (student['program'], 
                        student['major'], 
                        student['year'],
                        student['semester'], 
                        alphabetical_char), 
                        course['code'], 
                        'Lecture',
                        4, # equivalent of 2 
                        1))
                    _program_curriculum.append((
                        (student['program'], 
                        student['major'], 
                        student['year'], 
                        student['semester'],
                        alphabetical_char), 
                        course['code'], 
                        'Lecture',
                        2, # equivalent of 1
                        2))
                
    return _program_curriculum