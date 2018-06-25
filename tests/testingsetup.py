
import functools

all_tests = []

def test(func):
    all_tests.append(func)
    return func
    # @functools.wraps(func)
    # def testfunc(*args, **kwargs):

def execute():
    for test in all_tests:
        try:
            test()
        except Exception as e:
            print(e)

@test
def test_foo():
    print("in test_foo 1")

@test
def test_bar():
    print("in test_bar")

@test
def test_foo():
    print("in test_foo 2")

execute()
