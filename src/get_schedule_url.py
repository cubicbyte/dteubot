import os

def get_schedule_url(message, path='/cached-schedule'):
    structure_id = message.config['schedule']['structure_id']
    faculty_id = message.config['schedule']['faculty_id']
    course = message.config['schedule']['course']
    group_id = message.config['schedule']['group_id']
    
    if structure_id is None:
        structure_id = ''
    else:
        structure_id = structure_id + '-'
    
    url = os.getenv('API_URL') + path + f'/{structure_id}{faculty_id}-{course}-{group_id}'
    
    return url
