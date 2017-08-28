
def add_new_combination(form, session):
    record_to_add = {"browser": form.select_browser.data,
                     "platform": form.select_platform.data,
                     "version": form.select_version.data}
    if 'saved_combinations' in session:
        saved_combinations = session['saved_combinations']
        saved_combinations.append(record_to_add)
        session['saved_combinations'] = saved_combinations
    else:
        session['saved_combinations'] = [record_to_add]


def persist_run_inputs(form, session):
    session['username'] = str(form.username.data)
    session['accesskey'] = str(form.accesskey.data)
    session['tunnelname'] = str(form.tunnelname.data)
    session['urls'] = str(form.urls.data)
    session['commands'] = str(form.commands.data)


def clear_saved_combinations(session):
    session['saved_combinations'] = list()