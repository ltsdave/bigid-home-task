import os


def get_env_var(env_var_name: str) -> str:
    return os.environ[env_var_name]
