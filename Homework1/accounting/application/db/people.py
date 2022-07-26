from random import choice


def get_employees():
    names = ['James', 'Robert', 'John', 'Michael', 'David', 'William', 'Richard', 'Joseph', 'Thomas', 'Charles',
             'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
    surnames = ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'White', 'Harris', 'Martin', 'Davis', 'Wilson',
                'Cooper', 'Evans', 'King', 'Thomas', 'Baker', 'Green', 'Wright', 'Johnson', 'Edwards', 'Clark']
    for i in range(1, 11):
        print(f'{i}. {choice(names)} {choice(surnames)}')
