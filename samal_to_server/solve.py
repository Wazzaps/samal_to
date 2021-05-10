from ortools.sat.python import cp_model

import json
import copy
import math
from functools import reduce
import time


def solve(people, settings, shifts):
    model = cp_model.CpModel()

    # -- Data --
    for person in people:
        person['restricted_tasks'] = person.get('restricted_tasks', [])
        person['assigned_tasks'] = person.get('assigned_tasks', [])
        person['prefers_longer_sleep'] = person.get('prefers_longer_sleep', False)

    MIN_REST_PER_DAY = int(settings['min_rest_per_day'])
    LONGSLEEP_MIN_REST_PER_DAY = int(settings['longsleep_min_rest_per_day'])
    OVERTIME_INTERVAL_MIN = int(settings['overtime_interval_min'])
    OVERTIME_THRESHOLD = int(settings['overtime_threshold'])
    MAX_OVERTIME_INTERVALS = int(settings['max_overtime_intervals'])
    LONGSLEEP_MAX_OVERTIME_INTERVALS = int(settings['longsleep_max_overtime_intervals'])

    SUFFER_PER_OVERTIME_MIN = int(settings['suffer_per_overtime_min'])
    LONGSLEEP_SUFFER_PER_OVERTIME_MIN = int(settings['longsleep_suffer_per_overtime_min'])

    SUFFER_PER_OVERTIME = OVERTIME_INTERVAL_MIN * SUFFER_PER_OVERTIME_MIN
    LONGSLEEP_SUFFER_PER_OVERTIME = OVERTIME_INTERVAL_MIN * SUFFER_PER_OVERTIME_MIN


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


    # -- Create bool variable for each shift x person (will the person do this shift) --
    people_at_shift = [
        [
            model.NewBoolVar('person{}_shift{}'.format(person_i, shift_i))
            for shift_i in range(len(shifts))
        ]
        for person_i in range(len(people))
    ]


    # -- Create bool variable for each 15min x person (is working at that time) --
    people_is_working = [
        [
            model.NewBoolVar('person{}_isworking{}'.format(person_i, is_working_i))
            for is_working_i in range(max(0, int(max_end_time / OVERTIME_INTERVAL_MIN)))
        ]
        for person_i in range(len(people))
    ]


    # -- Create bool variable for each 15min x person (is working for too long) --
    people_overtime = [
        [
            model.NewBoolVar('person{}_overtime{}'.format(person_i, overtime_i))
            for overtime_i in range(max(0, int(max_end_time / OVERTIME_INTERVAL_MIN) - OVERTIME_THRESHOLD))
        ]
        for person_i in range(len(people))
    ]


    # -- Cost function --
    suffering_per_person = [
        sum(
            [shifts[i]['duration'] * shifts[i]['cost'] * shift_var for i, shift_var in enumerate(person_shifts)] +
            [
                (LONGSLEEP_SUFFER_PER_OVERTIME if people[person_idx]['prefers_longer_sleep'] else SUFFER_PER_OVERTIME)
                    * overtime_var for overtime_var in people_overtime[person_idx]
            ]
        )
        for person_idx, person_shifts in enumerate(people_at_shift)
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

        longsleep_options = []
        for window in range(0, (24*60) - LONGSLEEP_MIN_REST_PER_DAY + 5, 5):
            disallowed_shifts = [
                shift['id']
                for shift in relevant_shifts
                if does_overlap(shift, { 'time': 24*60*day + window, 'duration': LONGSLEEP_MIN_REST_PER_DAY })
            ]
            longsleep_options.append(disallowed_shifts)

        for person_idx, person_shifts in enumerate(people_at_shift):
            if people[person_idx]['prefers_longer_sleep']:
                tmp_boolvars = [model.NewBoolVar('') for _ in longsleep_options]

                for i, option in enumerate(longsleep_options):
                    model.Add(sum([person_shifts[shift] for shift in option]) == 0).OnlyEnforceIf(tmp_boolvars[i])
            else:
                tmp_boolvars = [model.NewBoolVar('') for _ in options]

                for i, option in enumerate(options):
                    model.Add(sum([person_shifts[shift] for shift in option]) == 0).OnlyEnforceIf(tmp_boolvars[i])

            model.Add(sum(tmp_boolvars) != 0)


    # -- Constraint: Overtime bad --
    for person_idx, work_intervals in enumerate(people_is_working):
        for interval_idx, is_working_var in enumerate(work_intervals):
            interval_count = interval_idx
            active_shifts = [
                people_at_shift[person_idx][shift['id']]
                for shift in shifts
                if does_overlap(shift, { 'time': interval_count * OVERTIME_INTERVAL_MIN, 'duration': OVERTIME_INTERVAL_MIN })
            ]

            model.Add(sum(active_shifts) != 0).OnlyEnforceIf(is_working_var)
            model.Add(sum(active_shifts) == 0).OnlyEnforceIf(is_working_var.Not())

    for person_idx, person_overtime in enumerate(people_overtime):
        for interval_idx, overtime_var in enumerate(person_overtime):
            interval_count = interval_idx + OVERTIME_THRESHOLD

            model.Add(sum(people_is_working[person_idx][interval_idx:interval_idx+OVERTIME_THRESHOLD+1]) == OVERTIME_THRESHOLD+1).OnlyEnforceIf(overtime_var)
            model.Add(sum(people_is_working[person_idx][interval_idx:interval_idx+OVERTIME_THRESHOLD+1]) != OVERTIME_THRESHOLD+1).OnlyEnforceIf(overtime_var.Not())


    # -- Constraint: Too much overtime denied --
    for day in range(math.ceil(max_end_time / (24 * 60))):
        for person_idx, person_overtime in enumerate(people_overtime):
            OVERTIME_INTERVALS_PER_DAY = 24 * int(60 / OVERTIME_INTERVAL_MIN)
            max_overtime = LONGSLEEP_MAX_OVERTIME_INTERVALS if people[person_idx]['prefers_longer_sleep'] else MAX_OVERTIME_INTERVALS
            model.Add(sum(
                person_overtime[
                    max(0, day * OVERTIME_INTERVALS_PER_DAY - OVERTIME_THRESHOLD)
                    :max(0, (day+1) * OVERTIME_INTERVALS_PER_DAY - OVERTIME_THRESHOLD)
                ]
            ) <= max_overtime)


    # -- Minimize suffering delta --
    total = sum(shift['duration'] * shift['cost'] for shift in shifts)
    avg = total // len(people)
    # print(f'Expected avg suffering: {avg}')
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
            print(f'Time: {int(time.time())}, Delta: {self.Value(delta)*2} (~{self.Value(delta)/100/60*2:0.03} hrs)')

        def solution_count(self):
            return self.__solution_count


    print('Solving...')

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 6

    timeout = settings.get('timeout', 5)
    if timeout > 10:
        timeout = 10

    solver.parameters.max_time_in_seconds = timeout
    ans = solver.SolveWithSolutionCallback(model, SolutionPrinter())

    result = {}
    if ans == cp_model.FEASIBLE:
        result['solution_type'] = 'Feasible'
    elif ans == cp_model.OPTIMAL:
        result['solution_type'] = 'Optimal'
    elif ans == cp_model.INFEASIBLE or ans == cp_model.UNKNOWN:
        result['solution_type'] = 'Infeasible'
        return result


    # -- Verify --
    result['shifts'] = [None for _ in range(len(shifts))]
    errors = []
    normal_suffers = []
    longsleep_suffers = []
    for person_idx, person in enumerate(people_at_shift):
        print('--------------------------')
        person_assignments = [solver.Value(v) for v in person]
        person_assignments_string = ''.join(map(str, person_assignments))
        print(f'Assign.: {person_assignments_string}')
        person_is_working = [solver.Value(v) for v in people_is_working[person_idx]]
        person_is_working_string = ''.join(map(str, person_is_working))
        print(f'Working:  {person_is_working_string}')
        person_overtime = [solver.Value(v) for v in people_overtime[person_idx]]
        person_overtime_string = ''.join(map(str, person_overtime))
        print(f'Overtime: {"0" * OVERTIME_THRESHOLD}{person_overtime_string}')

        # Save to result
        for i, assignment in enumerate(person_assignments):
            if assignment:
                result['shifts'][i] = person_idx

        # Verify non-overlap
        for i, assignment in enumerate(person_assignments):
            if assignment:
                task = shifts[i]
                for j, other_assignment in enumerate(person_assignments[i+1:]):
                    if other_assignment:
                        other_task = shifts[i+1+j]
                        if does_overlap(task, other_task):
                            errors.append(f'Person #{person_idx}\'s tasks overlapped: #{i} and #{i+1+j}')

        # Verify sleep time
        is_working = [0 for _ in range(max_end_time)]
        # is_working[12::24] = [1 for _ in range(len(is_working[12::24]))]  # Mark lunch as non-rest hour
        for i, assignment in enumerate(person_assignments):
            if assignment:
                task = shifts[i]
                is_working[task['time']:task['time'] + task['duration']] = [1 for _ in range(task['duration'])]

        minute_string = ''.join(map(str, is_working))
        # print(f'Work hrs: {minute_string[::60]}')
        consec_rest_min = max(len(s) for s in minute_string.split('1'))
        consec_work_min = max(len(s) for s in minute_string.split('0'))
        if consec_rest_min < MIN_REST_PER_DAY:
            errors.append(f'Person #{person_idx} has only {consec_rest_min / 60} hrs rest per day')
        work_mins = sum(shifts[i]['duration'] for i, assigned in enumerate(person_assignments) if assigned)
        print(f'Max Rest: {int(consec_rest_min/60)}:{str(consec_rest_min % 60).ljust(2, "0")}, '
            f'Max Work: {int(consec_work_min/60)}:{str(consec_work_min % 60).ljust(2, "0")}, '
            f'Total Work: {int(work_mins/60)}:{str(work_mins % 60).ljust(2, "0")}, '
            f'Suffer: {solver.Value(suffering_per_person[person_idx])}')

        if people[person_idx]['prefers_longer_sleep']:
            longsleep_suffers.append(solver.Value(suffering_per_person[person_idx]))
        else:
            normal_suffers.append(solver.Value(suffering_per_person[person_idx]))

    result['errors'] = errors
    result['trivia'] = {
        'suffering_delta': solver.Value(delta)*2,
        'suffering_delta_hrs_approx': solver.Value(delta)/100/60*2,
        'avg_normal_suffering': 0,
        'avg_longsleep_suffering': 0,
    }
    if normal_suffers:
        result['trivia']['avg_normal_suffering'] = sum(normal_suffers) // len(normal_suffers)
    if longsleep_suffers:
        result['trivia']['avg_longsleep_suffering'] = sum(longsleep_suffers) // len(longsleep_suffers)

    print('--------------------------')
    if errors:
        print('Errors:')
        for e in errors:
            print(f' - {e}')

    print(f'Delta: {result["trivia"]["suffering_delta"]} (~{result["trivia"]["suffering_delta_hrs_approx"]:0.03} hrs)')
    print(f'Avg normal suffer: {result["trivia"]["avg_normal_suffering"]}')
    print(f'Avg longsleep suffer: {result["trivia"]["avg_longsleep_suffering"]}')

    return result
