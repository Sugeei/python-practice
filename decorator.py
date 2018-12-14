# coding=utf-8

# assume these functions exist
def current_user_id():
    return 111
    """
    this function returns the current logged in user id, if the user is not authenticated then return None
    """


def get_permissions(user_id):
    if user_id > 1000:
        return ["premium_member"]
    elif user_id > 100:
        return ["administrator"]
    elif user_id > 10:
        return ["logged_in"]
    else:
        return []
    """
    returns a list of permission strings for the given user. For example ['logged_in','administrator','premium_member']
    """


def requires_admin(fn):
    def ret_fn(*args, **kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'administrator' in lPermissions:
            return fn(*args, **kwargs)
        else:
            raise Exception("Not allowed")

    return ret_fn


def requires_logged_in(fn):
    def ret_fn(*args, **kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'logged_in' in lPermissions:
            return fn(*args, **kwargs)
        else:
            raise Exception("Not allowed")

    return ret_fn


def requires_premium_member(fn):
    def ret_fn(*args, **kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'premium_member' in lPermissions:
            return fn(*args, **kwargs)
        else:
            raise Exception("Not allowed")

    return ret_fn


@requires_admin
def delete_user(iUserId):
    """
    delete the user with the given Id. This function is only accessable to users with administrator permissions
    """


@requires_logged_in
def new_game():
    """
    any logged in user can start a new game
    """


@requires_premium_member
def premium_checkpoint():
    """
    save the game progress, only accessable to premium members
    """


# it would be better to have one decorator that does the job of all above
def require_permission(strPermission):
    def decorator(fn):
        def ret_fn(*args, **kwargs):
            lPermissions = get_permissions(args[0])
            if strPermission in lPermissions:
                return fn(*args, **kwargs)
            raise Exception("permission denied")
        return ret_fn
    return decorator


@require_permission("administrator")
def delete_user(iUserId):
    """
    delete the user with the given Id. This function is only accessable to users with administrator permissions
    """


@require_permission("logged_id")
def new_game():
    """
    any logged in user can start a new game
    """


@require_permission("premium_member")
def premium_checkpoint():
    """
    save the game progress, only accessable to premium members
    """


# delete_user(1)
# delete_user(11)
delete_user(111)
# delete_user(1111)
