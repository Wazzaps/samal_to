from ortools.sat.python import cp_model

import copy
import math
from functools import reduce

model = cp_model.CpModel()

# -- Data --
people = [{
    'restricted_tasks': [],
    'assigned_tasks': [],
} for i in range(16)]

# people[0]['restricted_tasks'] = [32]
# people[0]['assigned_tasks'] = [0]

MIN_REST_PER_DAY = int(8.5 * 60)

shifts = [
    # Task A
    { 'time': int((12) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((16) * 60), 'duration': int((3) * 60), 'cost': 100 },
    { 'time': int((24+6) * 60), 'duration': int((1) * 60), 'cost': 100 },
    { 'time': int((24+11) * 60), 'duration': int((1) * 60), 'cost': 100 },

    # Task B
    { 'time': int((19) * 60), 'duration': int((3) * 60), 'cost': 100 },
    { 'time': int((22) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+2) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+6) * 60), 'duration': int((1) * 60), 'cost': 100 },

    # Task C
    { 'time': int((15) * 60), 'duration': int((3.5) * 60), 'cost': 100 },
    { 'time': int((15) * 60), 'duration': int((3.5) * 60), 'cost': 100 },
    { 'time': int((14.5) * 60), 'duration': int((5) * 60), 'cost': 100 },
    { 'time': int((24+6.5) * 60), 'duration': int((5) * 60), 'cost': 100 },
    { 'time': int((24+7) * 60), 'duration': int((4.5) * 60), 'cost': 100 },
    { 'time': int((24+7) * 60), 'duration': int((4.5) * 60), 'cost': 100 },

    # Task D
    { 'time': int((21) * 60), 'duration': int((2) * 60), 'cost': 100 },

    # Task E
    { 'time': int((20) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+4) * 60), 'duration': int((1) * 60), 'cost': 100 },

    # Task F
    { 'time': int((24+6+(5/6)) * 60), 'duration': int((2 + (1/6)) * 60), 'cost': 100 },
    { 'time': int((24+5) * 60), 'duration': int((2) * 60), 'cost': 100 },

    # Task G
    { 'time': int((12) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((16) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((20) * 60), 'duration': int((1) * 60), 'cost': 100 },

    # Task H
    { 'time': int((24+4) * 60), 'duration': int((2) * 60), 'cost': 100 },

    # Task I
    { 'time': int((24+6) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+10) * 60), 'duration': int((2) * 60), 'cost': 100 },

    # Task J
    { 'time': int((24+7) * 60), 'duration': int((3) * 60), 'cost': 100 },

    # Task K
    { 'time': int((24+8 + (2/6)) * 60), 'duration': int(60 + 40), 'cost': 100 },

    # Task L
    { 'time': int((20) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+4) * 60), 'duration': int((1) * 60), 'cost': 100 },

    # Task M
    { 'time': int((12) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((16) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((20) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+4) * 60), 'duration': int((4) * 60), 'cost': 100 },
    { 'time': int((24+8) * 60), 'duration': int((4) * 60), 'cost': 100 },
]


# -- Add indicies to tasks --
for i, shift in enumerate(shifts):
    shift['id'] = i


# -- Rebase time to first shift --
min_start_time = min(s['time'] for s in shifts)
for shift in shifts:
    shift['time'] -= min_start_time


# -- Calculate time bounds for work --
def end_time(task):
    return task['time'] + task['duration']

max_end_time = max(map(end_time, shifts))


# -- Create bool variable for each shift, for each person (will the person do this shift) --
people_at_shift = [
    [
        model.NewBoolVar('person{}_shift{}'.format(person_i, shift_i))
        for shift_i in range(len(shifts))
    ]
    for person_i in range(len(people))
]


# -- Cost function --
suffering_per_person = [
    sum([shifts[i]['duration'] * shifts[i]['cost'] * shift_var for i, shift_var in enumerate(person_shifts)])
    for person_shifts in people_at_shift
]


# -- Constraint: Each shift is fulfilled --
for shift_i in range(len(shifts)):
    model.Add(sum(person[shift_i] for person in people_at_shift) == 1)


# -- Constraint: No restricted tasks, Force assigned tasks --
for person_idx, person_shifts in enumerate(people_at_shift):
    for shift_idx, assignment in enumerate(person_shifts):
        if shift_idx in people[person_idx]['restricted_tasks']:
            model.Add(assignment == 0)
        if shift_idx in people[person_idx]['assigned_tasks']:
            model.Add(assignment == 1)


# -- Constraint: No overlap --
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


# -- Constraint: Sleep time --
for day in range(math.ceil(max_end_time / (24 * 60))):
    relevant_shifts = [shift for shift in shifts if does_overlap(shift, { 'time': 24*60*day, 'duration': 24*60 })]

    # 5 min window interval
    options = []
    for window in range(0, (24*60) - MIN_REST_PER_DAY + 5, 5):
        disallowed_shifts = [
            shift['id']
            for shift in relevant_shifts
            if does_overlap(shift, { 'time': 24*60*day + window, 'duration': MIN_REST_PER_DAY })
        ]
        options.append(disallowed_shifts)

    for person_shifts in people_at_shift:
        # for option in options:
        #     print(sum(person_shifts[i] for i in option) == 0)

        tmp_boolvars = [model.NewBoolVar('') for _ in options]

        for i, option in enumerate(options):
            model.Add(sum([person_shifts[shift] for shift in option]) == 0).OnlyEnforceIf(tmp_boolvars[i])

        model.Add(sum(tmp_boolvars) != 0)


# -- Constraint: No adjacent? --
# TODO


# -- Minimize suffering delta --
total = sum(shift['duration'] * shift['cost'] for shift in shifts)
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
        print(f'Delta: {self.Value(delta)} (~{self.Value(delta)/100/60*2:0.03} hrs)')

    def solution_count(self):
        return self.__solution_count


solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 8
solver.parameters.max_time_in_seconds = 2
ans = solver.SolveWithSolutionCallback(model, SolutionPrinter())

if ans == cp_model.FEASIBLE:
    print('Feasible')
elif ans == cp_model.OPTIMAL:
    print('Optimal')
elif ans == cp_model.INFEASIBLE:
    print('Infeasible')
    exit(1)

errors = []
for person_idx, person in enumerate(people_at_shift):
    print('--------------------------')
    person_assignments = [solver.Value(v) for v in person]
    person_assignments_string = ''.join(map(str, person_assignments))
    print(f'Assign.: {person_assignments_string}')

    # Verify non-overlap
    for i, assignment in enumerate(person_assignments):
        if assignment:
            task = shifts[i]
            for j, other_assignment in enumerate(person_assignments[i+1:]):
                if other_assignment:
                    other_task = shifts[i+1+j]
                    if does_overlap(task, other_task):
                        errors.append(f'Person #{person_idx}\'s Tasks overlapped: #{i} and #{i+1+j}')

    # Verify sleep time
    is_working = [0 for _ in range(max_end_time)]
    # is_working[12::24] = [1 for _ in range(len(is_working[12::24]))]  # Mark lunch as non-rest hour
    for i, assignment in enumerate(person_assignments):
        if assignment:
            task = shifts[i]
            is_working[task['time']:task['time'] + task['duration']] = [1 for _ in range(task['duration'])]

    minute_string = ''.join(map(str, is_working))
    print(f'Rest: {minute_string[::60]}')
    rest_min = max(len(s) for s in minute_string.split('1'))
    if rest_min < MIN_REST_PER_DAY:
        errors.append(f'Person #{person_idx} has only {rest_min / 60} hrs rest per day')
    work_mins = sum(shifts[i]['duration'] for i, assigned in enumerate(person_assignments) if assigned)
    print(f'Max Rest: {int(rest_min/60)}:{str(rest_min % 60).ljust(2, "0")}, Hrs: {work_mins/60}, Suf.: {solver.Value(suffering_per_person[person_idx])}')

print('--------------------------')
if errors:
    print('Errors:')
    for e in errors:
        print(f' - {e}')

print(f'Delta: {solver.Value(delta)} (~{solver.Value(delta)/100/60*2:0.03} hrs)')