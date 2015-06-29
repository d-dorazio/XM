"""Module that defines the endpoints by the api. To reach the api just do a
GET request to '<host>:<port>/api/' to get the list of all availables functions
and params. To call one of those do another GET request to
'<host>:<port>/api/<function>' and pass the parameters via query params.

If you run this file a debug server will be started.
"""
from flask import Flask, request, abort, jsonify
from flask.ext.cors import CORS

from brain import Brain, Body
from util import XMException

app = application = Flask(__name__)
cors = CORS(app, origins='*')

brain = Brain(Body())


@app.errorhandler(400)
def bad_request(err):
    """400 - Bad request error handler.

    Returns:
        str: the json representation of the error
    """
    return jsonify(
        {'success': False,
         'err_code': 400,
         'error': 'Bad request!'})


@app.errorhandler(404)
def not_found(err):
    """404 - Not found error handler.

    Returns:
        str: the json representation of the error
    """
    return jsonify({'success': False, 'err_code': 404, 'error': 'Not found!'})


@app.route('/api', methods=['GET'])
def get_help():
    """Main route that provides the documentation for the synapses.

    Returns:
        str: the json representation of all the availables commands
    """
    return jsonify({'success': True, 'data': brain.get_help()})


@app.route('/api/<cmd>', methods=['GET'])
def do_cmd(cmd):
    """Main route. According to which value `cmd` holds,
    the relative 'circuit' is called. Eventual parameters must be
    passed using query parameters. If the command isn't found, then
    404-not found. If a parameter passing error occured then 400-bad request.

    Args:
        cmd (str): function to call.

    Returns:
        str: the json representation of the response
    """
    try:
        brain.call(cmd, **request.args.to_dict(flat=True))
        return jsonify({'success': True})
    except XMException as exc:
        return jsonify({'success': False, 'error': str(exc)})
    except TypeError:
        abort(400)
    except KeyError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
