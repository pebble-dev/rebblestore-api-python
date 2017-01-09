from flask import abort, Blueprint, jsonify, render_template
# flcom sqlalchemy_searchable import search as vector_search

from ..models import Application, get_db

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/apps')
def render_root():
    Session, db = get_db()
    session = Session()
    applications = [x.to_json() for x in session.query(Application).all()]

    rv = {
        'applications': applications
    }

    return jsonify(**rv)


@bp.route('/apps/<guid>')
def render_app_page(guid):
    # TODO: error handling here (ensure guid is a guid)
    session, db = get_db()

    app = session.query(Application).filter(Application.guid == guid).first()
    if not app:
        abort(404)

    return render_template('app.html', app=app)
