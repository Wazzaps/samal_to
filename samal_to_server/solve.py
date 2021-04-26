from ortools.sat.python import cp_model

import copy

model = cp_model.CpModel()

people = [chr(ord('A') + i) for i in range(16)]

shifts = [
    # Task A
    { 'time': int((12) * 60), 'duration': int((4) * 60) },
    { 'time': int((16) * 60), 'duration': int((3) * 60) },
    { 'time': int((24+6) * 60), 'duration': int((1) * 60) },
    { 'time': int((24+11) * 60), 'duration': int((1) * 60) },

    # Task B
    { 'time': int((19) * 60), 'duration': int((3) * 60) },
    { 'time': int((22) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+2) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+6) * 60), 'duration': int((1) * 60) },

    # Task C
    { 'time': int((15) * 60), 'duration': int((3.5) * 60) },
    { 'time': int((15) * 60), 'duration': int((3.5) * 60) },
    { 'time': int((14.5) * 60), 'duration': int((5) * 60) },
    { 'time': int((24+6.5) * 60), 'duration': int((5) * 60) },
    { 'time': int((24+7) * 60), 'duration': int((4.5) * 60) },
    { 'time': int((24+7) * 60), 'duration': int((4.5) * 60) },

    # Task D
    { 'time': int((21) * 60), 'duration': int((2) * 60) },

    # Task E
    { 'time': int((20) * 60), 'duration': int((4) * 60) },
    { 'time': int((24) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+4) * 60), 'duration': int((1) * 60) },

    # Task F
    { 'time': int((24+6+(5/6)) * 60), 'duration': int((2 + (1/6)) * 60) },
    { 'time': int((24+5) * 60), 'duration': int((2) * 60) },

    # Task G
    { 'time': int((12) * 60), 'duration': int((4) * 60) },
    { 'time': int((16) * 60), 'duration': int((4) * 60) },
    { 'time': int((20) * 60), 'duration': int((1) * 60) },

    # Task H
    { 'time': int((24+4) * 60), 'duration': int((2) * 60) },

    # Task I
    { 'time': int((24+6) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+10) * 60), 'duration': int((2) * 60) },

    # Task J
    { 'time': int((24+7) * 60), 'duration': int((3) * 60) },

    # Task K
    { 'time': int((24+8 + (2/6)) * 60), 'duration': int(60 + 40) },

    # Task L
    { 'time': int((20) * 60), 'duration': int((4) * 60) },
    { 'time': int((24) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+4) * 60), 'duration': int((1) * 60) },

    # Task M
    { 'time': int((12) * 60), 'duration': int((4) * 60) },
    { 'time': int((16) * 60), 'duration': int((4) * 60) },
    { 'time': int((20) * 60), 'duration': int((4) * 60) },
    { 'time': int((24) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+4) * 60), 'duration': int((4) * 60) },
    { 'time': int((24+8) * 60), 'duration': int((4) * 60) },
]

people_at_shift = [
    [
        model.NewBoolVar('person{}_shift{}'.format(person_i, shift_i))
        for shift_i in range(len(shifts))
    ]
    for person_i in range(len(people))
]

suffering_per_person = [
    sum([shifts[i]['duration'] * shift_var for i, shift_var in enumerate(person_shifts)])
    for person_shifts in people_at_shift
]

# -- Each shift is fulfilled --
for shift_i in range(len(shifts)):
    model.Add(sum(person[shift_i] for person in people_at_shift) == 1)

# -- No overlap --
def end_time(task):
    return task['time'] + task['duration']

def does_overlap(task_a, task_b):
    return end_time(task_a) > task_b['time'] and end_time(task_b) > task_a['time']

for person_shifts in people_at_shift:
    for i, assignment in enumerate(person_shifts):
        task = shifts[i]
        for j, other_assignment in enumerate(person_shifts[i+1:]):
            other_task = shifts[i+1+j]
            if does_overlap(task, other_task):
                # print((assignment + other_assignment) != 2)
                model.Add((assignment + other_assignment) != 2)

# -- Sleep time --
# -- No adjacent? --

# -- Minimize suffering delta --
total = sum(shift['duration'] for shift in shifts)
avg = total // len(people)
delta = model.NewIntVar(0, total, "delta")

for suffering in suffering_per_person:
    model.Add(suffering >= avg - delta)
    model.Add(suffering <= avg + delta)

model.Minimize(delta)

# -- Solve --
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__()
        # self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print('Delta:', self.Value(delta))

    def solution_count(self):
        return self.__solution_count


solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 8
solver.parameters.max_time_in_seconds = 5
ans = solver.SolveWithSolutionCallback(model, SolutionPrinter())
# ans = solver.Solve(model)

if ans == cp_model.FEASIBLE:
    print('Feasible')
elif ans == cp_model.OPTIMAL:
    print('Optimal')
elif ans == cp_model.INFEASIBLE:
    print('Infeasible')

for i, person in enumerate(people_at_shift):
    print('--------------------------')
    person_assignments = [solver.Value(v) for v in person]
    print(f'{person_assignments} suf:{solver.Value(suffering_per_person[i])}')

    # Verify non-overlap
    for i, assignment in enumerate(person_assignments):
        if assignment:
            task = shifts[i]
            for j, other_assignment in enumerate(person_assignments[i+1:]):
                if other_assignment:
                    other_task = shifts[i+1+j]
                    if does_overlap(task, other_task):
                        print(f'Tasks overlapped: #{i} and #{i+1+j}')

    # Verify sleep time
    min_start_time = min(s['time'] for s in shifts)
    max_end_time = max(map(end_time, shifts))
    is_working = [0 for _ in range(max_end_time)]
    # is_working[12::24] = [1 for _ in range(len(is_working[12::24]))]  # Mark lunch as non-rest hour
    for i, assignment in enumerate(person_assignments):
        if assignment:
            task = shifts[i]
            is_working[task['time']:task['time'] + task['duration']] = [1 for _ in range(task['duration'])]

    minute_string = ''.join(map(str, is_working))[min_start_time:]
    print(minute_string[::60])
    rest_min = max(len(s) for s in minute_string.split('1'))
    print(f'Longest rest: {int(rest_min/60)}:{str(rest_min % 60).ljust(2, "0")}')

print('Delta:', solver.Value(delta))