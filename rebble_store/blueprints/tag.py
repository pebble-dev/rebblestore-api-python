from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args
from flask_restful import Api, Resource

from ..models import Collection, get_db

bp = Blueprint('tag', __name__, url_prefix='/tags')
api = Api(bp)

get_args = {
    'count': fields.Int(required=False, default=12),
}


class Tags(Resource):
    @use_args(get_args)
    def get(self, args):
        count = args.get('count', 12)
        session, _ = get_db()
        query = session.query(Collection).filter(
            Collection.type == 'tag').limit(count)

        return {'results': [x.to_json() for x in query]}


api.add_resource(Tags, '/')
