def get_username_from_session(session):
    return session['username']


def get_access_key_from_session(session):
    return session['accesskey']


def get_tunnelname_from_session(session):
    return session['tunnelname']


def get_combinations_from_session(session):
    return session['saved_combinations']


def get_urls_from_session(session):
    return str(session['urls']).split(',')


def get_commands_from_session(session):
    return session['commands'].split('\r\n')
