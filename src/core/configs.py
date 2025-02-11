def partial_update(user_data: dict, existing_config: dict):
    """
    This function updates objects depending on their types
    """
    for k in user_data:
        if isinstance(user_data[k], list) and isinstance(existing_config[k], list):
            existing_config[k].extend(user_data[k])
        elif isinstance(user_data[k], dict) and isinstance(existing_config[k], dict):
            existing_config[k].update(user_data[k])
        elif isinstance(user_data[k], str) and isinstance(existing_config[k], str):
            existing_config[k] = user_data[k]


def rename_global_keyword(user_data) -> None:
    """ "
    This function replaces the key 'global_' with 'global'
    from the user's input, since Python does not allow a
    key with the name 'global'
    """
    if "global_" in user_data:
        user_data["global"] = user_data["global_"]
        del user_data["global_"]
