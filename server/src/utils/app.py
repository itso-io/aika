from os import getenv

from flask import Flask, json
from sqlalchemy.ext.declarative import DeclarativeMeta

from utils.enums import APIErrorTypes

app = Flask(__name__)


class APIError(Exception):
    pass


def new_alchemy_encoder(revisit_self=False):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):

        def field_condition(self, x):
            return not x.startswith('_') and \
                   x != 'metadata' and \
                   x != 'query' and \
                   x != 'query_class'

        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}

                # TODO filter out non supported objects like functions
                for field in [x for x in dir(obj) if self.field_condition(x)]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def dump_json(*args, **kwargs):
    indent = None
    separators = (',', ':')

    if app.config['JSONIFY_PRETTYPRINT_REGULAR'] or app.debug:
        indent = 2
        separators = (', ', ': ')

    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args '
                        'and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    data = json.dumps(data, cls=new_alchemy_encoder(False),
                      check_circular=False,
                      indent=indent,
                      separators=separators) + '\n'
    return data


def jsonify(*args, **kwargs):
    """This function wraps :func:`dumps` to add a few enhancements that make
    life easier.  It turns the JSON output into a :class:`~flask.Response`
    object with the :mimetype:`application/json` mimetype.  For convenience, it
    also converts multiple arguments into an array or multiple keyword
    arguments
    into a dict.  This means that both ``jsonify(1,2,3)`` and
    ``jsonify([1,2,3])`` serialize to ``[1,2,3]``.

    For clarity, the JSON serialization behavior has the following differences
    from :func:`dumps`:

    1. Single argument: Passed straight through to :func:`dumps`.
    2. Multiple arguments: Converted to an array before being passed to
       :func:`dumps`.
    3. Multiple keyword arguments: Converted to a dict before being passed to
       :func:`dumps`.
    4. Both args and kwargs: Behavior undefined and will throw an exception.

    Example usage::

        from flask import jsonify

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }


    .. versionchanged:: 0.11
       Added support for serializing top-level arrays. This introduces a
       security risk in ancient browsers. See :ref:`json-security` for details.

    This function's response will be pretty printed if the
    ``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to True or the
    Flask app is running in debug mode. Compressed (not pretty) formatting
    currently means no indents and no spaces after separators.

    .. versionadded:: 0.2
    """
    response_body = dump_json(*args, **kwargs)

    return app.response_class(
        response_body,
        mimetype=app.config['JSONIFY_MIMETYPE']
    )
