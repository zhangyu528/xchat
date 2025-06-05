

def test_system_user_exists(system_user):
    assert system_user.username == "system_bot"
    assert system_user.is_system_user is True
