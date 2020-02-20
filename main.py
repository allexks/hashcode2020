#!/usr/local/bin/python3

import sys
from functools import cmp_to_key

# Classes


class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __repr__(self):
        return f"<Book #{self.id}: {self.score} pts>"


class Library:
    def __init__(self, id, books_count, days_sign_up, day_scan_max, books_set):
        self.id = id
        self.books_count = books_count
        self.days_sign_up = days_sign_up
        self.day_scan_max = day_scan_max
        self.books_set = books_set

    def __repr__(self):
        return f"<Library #{self.id}: {self.days_sign_up} days sign-up, {self.day_scan_max} books per day>"

    def priority(self):
        addition = 1 if self.books_count % self.day_scan_max > 0 else 0
        return self.days_sign_up + (self.books_count // self.day_scan_max) + addition

    def max_possible_books(self):
        addition = 1 if self.books_count % self.day_scan_max > 0 else 0
        return (self.books_count // self.day_scan_max + addition) * self.day_scan_max


# Arguments
USAGE_HELP_MSG = """Usage:
\t$ python3 {0} x
where in/x is the input filepath and out/x is the output filepath"""

if len(sys.argv) != 2:
    print(USAGE_HELP_MSG.format(sys.argv[0]))
    exit(1)

filename = sys.argv[1].lower()


# Input
all_input = []
with open(f"in/{filename}", "r") as fin:
    all_input = fin.readlines()

LIBRARIES = []

first_line = all_input[0]
scores_line = all_input[1]
library_lines = all_input[2:]

B, L, D = list(map(int, first_line.split()))
SCORES = list(map(int, scores_line.split()))

for lib_id in range(len(library_lines) // 2):
    first_row = library_lines[lib_id * 2]
    second_row = library_lines[lib_id * 2 + 1]
    n, t, m = list(map(int, first_row.split()))
    book_set = set(map(lambda x: Book(int(x), SCORES[int(x)]), second_row.split()))
    LIBRARIES.append(Library(lib_id, n, t, m, book_set))


# print(LIBRARIES)
# print(LIBRARIES[0].books_set)
# print(LIBRARIES[1].books_set)


# Algo

def compare_lib(lib1, lib2):
    """
    lib1 < lib2 => return -1
    lib1 == lib2 => return 0
    lib1 > lib2 => return 1
    """
    diff = abs(lib1.days_sign_up - lib2.days_sign_up)
    lib_min = sorted([lib1, lib2], key=lambda l: l.days_sign_up)[0]
    lib_min_first_diff_books = set(sorted(list(lib_min.books_set), key=lambda b: b.score, reverse=True)[:diff])
    lib1_after = lib1.books_set - lib_min_first_diff_books
    lib2_after = lib2.books_set - lib_min_first_diff_books
    first_score = sum(map(lambda b: b.score, lib1_after))
    second_score = sum(map(lambda b: b.score, lib2_after))
    max_score_lib = lib1_after if first_score >= second_score else lib2_after
    global D
    max_score_lib_ref = lib1 if max_score_lib == lib1_after else lib2
    first_of_max = (D - 1 - max(lib1.days_sign_up, lib2.days_sign_up)) * max_score_lib_ref.day_scan_max
    final_set = set(sorted(list(max_score_lib_ref.books_set), key=lambda b: b.score, reverse=True)[:first_of_max])
    min_score_lib = lib1_after if first_score < second_score else lib2_after
    smin = sum(map(lambda b: b.score, min_score_lib - final_set))
    final_set_score = sum(map(lambda b: b.score, final_set))
    if final_set_score > smin:
        if max_score_lib == lib1_after:
            return 1
        else:
            return -1
    else:
        if min_score_lib == lib1_after:
            return 1
        else:
            return -1


libraries_prioritized = sorted(LIBRARIES, key=cmp_to_key(compare_lib), reverse=False)
# print(libraries_prioritized)

libraries_signed = []
libraries_left = libraries_prioritized.copy()

# scanned_ids = dict([(id, False) for id in range(B)])

scanned_books_set = set()

outputlines = []
days_passed = 0
lib_index = 0
while days_passed < D:
    library = libraries_prioritized[lib_index]
    all_books_dict = dict([(b.id, b) for b in library.books_set])
    books_scanned_list = sorted(list(library.books_set), key=lambda b: b.score, reverse=True)
    first_row = "{0} {1}"

    if (D - 1) - library.priority() - days_passed > 0:
        pass
    else:
        all_needed = set(map(lambda b: b.id, books_scanned_list)) - scanned_books_set
        all_needed_books = list(map(lambda id: all_books_dict[id], all_needed))
        books_scanned_list = sorted(all_needed_books, key=lambda b: b.score, reverse=True)

    outputlines.append(first_row.format(library.id, len(books_scanned_list)))
    outputlines.append(" ".join(map(lambda b: str(b.id), books_scanned_list)))

    scanned_books_set = scanned_books_set | set(map(lambda b: b.id, books_scanned_list))

    days_passed += library.priority()
    lib_index += 1

outputlines = [f"{lib_index}"] + outputlines

# Output
with open(f"out/{filename}", "w") as fout:
    fout.write("\n".join(outputlines))
