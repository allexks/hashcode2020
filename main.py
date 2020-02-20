#!/usr/local/bin/python3

import sys
import networkx as nx

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

libraries_prioritized = sorted(LIBRARIES, key=lambda l: l.priority())

libraries_signed = []
libraries_left = libraries_prioritized.copy()

outputlines = []
days_passed = 0
lib_index = 0
while days_passed < D - 1:
    library = libraries_prioritized[lib_index]
    books = sorted(list(library.books_set), key=lambda b: b.score, reverse=True)
    books_scanned = len(books)
    first_row = "{0} {1}"

    if (D - 1) - library.priority() - days_passed > 0:
        pass
    else:
        books_scanned = D - 1 - library.days_sign_up

    book_scanned_list = books[:books_scanned]
    outputlines.append(first_row.format(library.id, len(book_scanned_list)))
    outputlines.append(" ".join(map(lambda b: str(b.id), book_scanned_list)))

    days_passed += library.priority()
    lib_index += 1

outputlines = [f"{lib_index}"] + outputlines

# Output
with open(f"out/{filename}", "w") as fout:
    fout.write("\n".join(outputlines))
