from flask import Flask, g


def teardown_session(response_or_exception):
    if hasattr(g, 'db'):
        g.db[0].remove()
    return response_or_exception


def register_blueprints(app, mod, bp_var_name):
    rv = []
    submods = {x for x in dir(mod) if not x[:2] == '__'}
    for submod in submods:
        submod = getattr(mod, submod)
        try:
            bp = getattr(submod, bp_var_name)
        except AttributeError:
            continue
        app.register_blueprint(bp)
        rv.append(bp)
    return rv


def create_app(config='app_debug.cfg'):
    from . import blueprints

    app = Flask(__name__)
    if config:
        app.config.from_pyfile(config)
    register_blueprints(app, blueprints, 'bp')
    app.teardown_appcontext_funcs = [teardown_session]
    return app
