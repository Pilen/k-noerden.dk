from pytest import raises
from knoerden.lib import user, config, utils

def test_create_user1(app):
    user.create_user("Pilen", "Søren Pilgård", "abc", "foo@example.com")

def test_create_user2(app):
    user.create_user("abe","Fornavn Efternavn","abc", "foo@example.com")
    with raises(utils.AbortException):
        user.create_user("Abe","Fornavn Efternavn","abc", "foo@example.com")

def test_password():
    raw_password = "abc"
    password = user.password_hash(raw_password)
    assert password != raw_password
    assert password
    assert user.password_check(raw_password, password)

def test_valid_username():
    assert not user.valid_username("")
    assert not user.valid_username(" ")
    assert not user.valid_username("12")
    assert not user.valid_username("-")
    assert user.valid_username("abc")
    assert user.valid_username("abc1")
    assert user.valid_username("1abc")
    assert user.valid_username("1abc2")

def test_valid_password():
    assert not user.valid_password("")
    assert user.valid_password("hunter2")

    password = ("a" * config.PASSWORD_MIN_LENGTH)
    assert not user.valid_password(password[1:])
    assert user.valid_password(password)

# def test_login(client):
#     response = client.post("/users/login/", data={"username": "pilen",
#                                                   "password": "abc"})
#     assert response.status_code >= 300 and response.status_code < 400
