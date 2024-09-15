import bcrypt


def hash_pwd(password: str):
    """generate hash from password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_pwd(password, pwd_hash):
    """checks the hash from the database with the user's password"""
    return bcrypt.checkpw(password.encode("utf-8"), pwd_hash)
