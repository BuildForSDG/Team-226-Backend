import pytest
from django.contrib.auth.models import User, Group, Permission


@pytest.fixture
def user_A(db) -> User:
    return User.objects.create_user("A")


@pytest.fixture
def user_B(db) -> Group:
    group = Group.objects.create(name="app_user")
    change_user_permissions = Permission.objects.filter(
        codename__in=["change_user", "view_user"],
    )
    group.permissions.add(*change_user_permissions)
    user = User.objects.create_user("B")
    user.groups.add(group)
    return user


def test_should_check_password(db, user_A: User) -> None:
    user_A.set_password("secret")
    assert user_A.check_password("secret") is True


def test_should_not_check_unusable_password(db, user_A: User) -> None:
    user_A.set_password("secret")
    user_A.set_unusable_password()
    assert user_A.check_password("secret") is False


def test_should_create_user(user_B: User) -> None:
    assert user_B.username == "B"


def test_user_is_in_app_user_group(user_B: User) -> None:
    assert user_B.groups.filter(name="app_user").exists()


def test_should_create_two_users(user_A: User, user_B: User) -> None:
    assert user_A.pk != user_B.pk
