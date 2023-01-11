#This program serves workers on a shifts schedule
# Data: there are 3 shifts (s), 5 workers (w), 7 days (d)
# each worker has one shift per day


from ortools.sat.python import cp_model


def main():
    # Data.
    num_workers = 5
    num_shifts = 3
    num_days = 7
    all_workers = range(num_workers)
    all_shifts = range(num_shifts)
   
    all_days = range(num_days)

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: worker 'w' works shift 's' on day 'd'.
    shifts = {}
    for w in all_workers:
        for d in all_days:
            for s in all_shifts:
                shifts[(w, d,
                        s)] = model.NewBoolVar('shift_w%id%is%i' % (w, d, s))

    # Each shift is assigned to exactly one worker in the schedule period.
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts[(w, d, s)] for w in all_workers)

    # Each worker works at most one shift per day.
    for w in all_workers:
        for d in all_days:
            model.AddAtMostOne(shifts[(w, d, s)] for s in all_shifts)

    # Try to distribute the shifts evenly, so that each worker works
    # min_shifts_per_worker shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of workers, some workers will
    # be assigned one more shift.
    min_shifts_per_worker = (num_shifts * num_days) // num_workers
    if num_shifts * num_days % num_workers == 0:
        max_shifts_per_worker = min_shifts_per_worker
    else:
        max_shifts_per_worker = min_shifts_per_worker + 1
    for w in all_workers:
        shifts_worked = []
        for d in all_days:
            for s in all_shifts:
                shifts_worked.append(shifts[(w, d, s)])
        model.Add(min_shifts_per_worker <= sum(shifts_worked))
        model.Add(sum(shifts_worked) <= max_shifts_per_worker)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True


    class WorkersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""

        def __init__(self, shifts, num_workers, num_days, num_shifts, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_workers = num_workers
            self._num_days = num_days
            self._num_shifts = num_shifts
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            self._solution_count += 1
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                print('Day %i' % d)
                for w in range(self._num_workers):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(w, d, s)]):
                            is_working = True
                            print('  Worker %i works shift %i' % (w, s))
                    if not is_working:
                        print('  Worker {} does not work'.format(w))
            if self._solution_count >= self._solution_limit:
                print('Stop search after %i solutions' % self._solution_limit)
                self.StopSearch()

        def solution_count(self):
            return self._solution_count

    # Display the first five solutions.
    solution_limit = 5
    solution_printer = WorkersPartialSolutionPrinter(shifts, num_workers,
                                                    num_days, num_shifts,
                                                    solution_limit)

    solver.Solve(model, solution_printer)

    # Statistics.
    print('\nStatistics')
    print('  - conflicts      : %i' % solver.NumConflicts())
    print('  - branches       : %i' % solver.NumBranches())
    print('  - wall time      : %f s' % solver.WallTime())
    print('  - solutions found: %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()
