"""User Controller"""
from model.users import UserDetails

from controller.database_controller import check_if_user_exists, create_user


def check_user(user_details : UserDetails):
    """Check if the user is exists"""
    return check_if_user_exists(user_details)

def setup_user(user_details : UserDetails):
    """Create a new user"""
    return create_user(user_details)
