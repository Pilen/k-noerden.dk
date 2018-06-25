
# from . import test

# class TestUser(test.Base):
#     def test_b(self):
#         print("test b")

#     def test_a(self):
#         print("test a")



# leak = []
# import pytest

# @pytest.fixture
# def foo():
#     obj = object()
#     leak.append(obj)
#     print("foo created")
#     return obj

# @pytest.fixture
# def bar(foo):
#     return foo

# def test_B(foo, bar):
#     print("test B", foo, bar)

# def test_A(foo):
#     print("test A", foo)


# def test_A():
#     print("other A")
