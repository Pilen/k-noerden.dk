#!/usr/bin/env bash

source venv/bin/activate

python -m scripts.reset_database;

time python -m cProfile -s tottime $(which pytest) -s tests/test.py > profile-test-results.txt


# time python -m cProfile -s tottime -o profile-test-results.txt tests/test.py
# python -c "import pstats; pstats.Stats('profile-test-results.txt').strip_dirs().sort_stats('tottime').print_stats()" | less
