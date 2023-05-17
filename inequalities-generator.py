def generate_substrings(string: str, length, cyclic=False):
    if cyclic:
        tail = string
        while len(tail) < length - 1:
            tail += string
        long_string = string + tail
        return [long_string[i:i + length] for i in range(len(string))]
    return [string[i:i + length] for i in range(len(string) - length + 1)]


def substring_statistics(left_column, right_column, length):
    stats = {}
    for row in range(len(left_column)):
        left_str = left_column[row].expanded
        right_str = right_column[row].replace('c', 'Aa')
        for substring in generate_substrings(left_str, length):
            if substring in stats:
                stats[substring]['positive_rows'].add(row)
            else:
                stats[substring] = {'positive_rows': {row}, 'negative_rows': set()}
        for substring in generate_substrings(right_str, length):
            if substring in stats:
                stats[substring]['negative_rows'].add(row)
            else:
                stats[substring] = {'positive_rows': set(), 'negative_rows': {row}}
    return stats


word_z = 'ABBBaBAbbabbbAbaBB'


def eliminate_rows(statistics: dict[str, dict[str, set]], row_set: set, length):
    keys = statistics.keys()
    essential_keys = [key for key in keys if
                      key not in generate_substrings(word_z, length, cyclic=True) and 'b' in key.lower()]
    elimination_needed = True
    while row_set and elimination_needed:
        redundant_rows = set()
        for key in essential_keys:
            plus_set = statistics[key]['positive_rows']
            minus_set = statistics[key]['negative_rows']
            if not plus_set or not minus_set:
                redundant_rows.update(plus_set, minus_set)
        if not redundant_rows:
            elimination_needed = False
        else:
            row_set.difference_update(redundant_rows)
            for key in keys:
                statistics[key]['positive_rows'].difference_update(redundant_rows)
                statistics[key]['negative_rows'].difference_update(redundant_rows)
    return row_set


@lru_cache(maxsize=None)
def generate_columns(n):
    initial_strings = ['Abb', 'ABa', 'BBa', 'Aba', 'BBcbb', 'aBcbb', 'BBcbA', 'aBcbA']
    if n == 2:
        left_column = [Word(string) for string in initial_strings]
        right_column = [word.without_specials for word in left_column]
        return left_column, right_column
    if n > 2:
        c_insertion = n % 2 == 0
        columns = generate_columns(n - 1)
        left_column = list(dict.fromkeys(
            list(reduce(lambda l1, l2: l1 + l2, [word.get_derived_words(c_insertion) for word in columns[0]]))))
        right_column = [word.without_specials for word in left_column]
        stats = substring_statistics(left_column, right_column, n)
        row_set = sorted(eliminate_rows(stats, set(range(len(left_column))), n))
        left_column = [left_column[row] for row in row_set]
        right_column = [right_column[row] for row in row_set]
        return left_column, right_column


def search_for_special_row(n):
    column = generate_columns(n)[0]
    for row in range(len(column)):
        string = column[row].expanded
        if string in generate_substrings(word_z, len(string), cyclic=True):
            return row
    return -1


def get_rows(n):
    left_column, right_column = generate_columns(n)
    return [(left_column[i].expanded, right_column[i].replace('c', 'Aa')) for i in range(len(left_column))]


def print_columns(n):
    left_column, right_column = generate_columns(n)
    row_count = len(left_column)
    print(f'Reduced system for n={n}:\n')
    for row in range(row_count):
        print(left_column[row].with_dots + '\t\t\t\t' + right_column[row])
    print(f'\nNumber of rows: {row_count}')


def print_rows(n):
    print(f'Reduced system for n={n} (first row is special):\n')
    for row in get_rows(n):
        print(row)
    print(f'\nNumber of rows: {len(get_rows(n))}')


def generate_system_of_inequalities(n):
    rows = get_rows(n)
    special_row = search_for_special_row(n)
    program = MixedIntegerLinearProgram(solver="PPL")
    variables = program.new_variable(integer=True)
    constraints = [program.sum(variables[key] for key in generate_substrings(pair[0], n)) - program.sum(
        variables[key] for key in generate_substrings(pair[1], n)) for pair in rows]
    if special_row == -1:
         print("Stop")
    else:
        program.add_constraint(constraints[special_row], max=-1)
    for constraint in constraints:
        program.add_constraint(constraint, max=0)
    for word in generate_substrings(word_z, n, cyclic=True):
        program.add_constraint(variables[word] == 0)
    for key in variables.keys():
        if set(key).issubset({'a', 'A'}):
            program.add_constraint(variables[key] == 0)
    return program, variables


def show_system(n):
    program = generate_system_of_inequalities(n)[0]
    program.show()


def solve_system(n):
    program, variables = generate_system_of_inequalities(n)
    program.solve()
    print(program.get_values(variables))
