"""setup system path"""
import sys


def setup_path():
    """setup_path"""
    sys.path.append('..')
    sys.path.append('/backend')
    sys.path.append('/backend/auth')
    sys.path.append('/backend/db')
    sys.path.append('/backend/model')
    sys.path.append('/backend/controller')
    sys.path.append('/backend/utils')
