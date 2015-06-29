"""This module is core of the rover, because through
the `Brain` you can use the functionalities of the hole
body.

Attributes:
    DEFAULT_PORT (str): default serial port `Legs` will use.
        By default it is '/dev/ttyACM0'

Example:
    $ body = Body()
    $ brain = Brain(Body)
    $ brain.call('forward', async=True)
"""

import os
import datetime

from leg import Legs
from eyes import Eyes
from mouth import Mouth
from util import LockAdapter, str_to_bool, str_to_int

DEFAULT_PORT = '/dev/ttyACM0'


def move_synapse(async=None):
    """Synapse to adapt an async string to a boolean. Internally it calls
    `str_to_bool` so refer to it for a general overview.

    Args:
        async (str, default None): string either containing a boolean or an
            integer.

    Returns:
        ([bool], {}): a tuple of args and kwargs. The last one is always empty
    """
    res = [str_to_bool(async)] if async else []
    return res, {}


def speedvalue_synapse(speed_value):
    """Synapse to adapt a speed value string to an integer. Internally it calls
    `str_to_int` so refer to it for a general overview.

    Args:
        speed_value (str): string representation of an integer.

    Returns:
        ([bool], {}): a tuple of args and kwargs. The last one is always empty.
    """
    res = [str_to_int(speed_value)] if speed_value else []
    return res, {}


def movetime_synapse(time):
    """Synapse to adapt a time string to an integer. Internally it calls
    `str_to_int` so refer to it for a general overview.

    Args:
        speed_value (str): string representation of an integer.

    Returns:
        ([bool], {}): a tuple of args and kwargs. The last one is always empty.
    """
    res = [str_to_int(time)] if time else []
    return res, {}


def say_synapse(text, amplitude=None, wpm=None):
    """Synapse to adapt the parameters of say.

    Args:
        text (str): text to reproduce.
		amplitude(int, optional): string representation of an integer.
		wpm(int, optional): string representation of an integer.

    Returns:
        ([str, int, int], {}): a tuple of args and kwargs. The last one is always empty.
    """
    res = [text]
    res += [str_to_int(amplitude)] if amplitude else []
    res += [str_to_int(wpm)] if wpm else []
    return res, {}


class Body:
    """Body is the container of several parts such as Legs and Mouth.
    Body has a network of 'circuits' made by synapses. Each circuit
    is a path to a given 'target'(aka method of a part
    of the body) preceded and followed by other functions to provide
    flexibility(aka synapses).
    To add new part to the `Body` you can use inheritance or just
    create the desired objects in `Body` and add the desidered synapses.
    """

    def __init__(self, port=DEFAULT_PORT, logdir='/var/log/xm'):
        """Creates a new istance of the body. By default it's composed by
        a thread-safe version of `Legs`, `Mouth` and `Eyes`.

        Args:
            port (str): serial port `Legs` will connect to.
            logdir (str): path where to store logs.
        """
        self.safe_legs = LockAdapter(Legs(port))

        eye_log = '{}-eyes.log'.format(str(datetime.date.today()))
        self.safe_mouth = Mouth()
        self.safe_eye = Eyes(log=open(os.path.join(logdir, eye_log), 'w'))

        self.circuits = {}

        self.add_circuit('forward',
                         target=self.safe_legs.forward,
                         pre=[move_synapse])
        self.add_circuit('backward',
                         target=self.safe_legs.backward,
                         pre=[move_synapse])
        self.add_circuit('left',
                         target=self.safe_legs.left,
                         pre=[move_synapse])
        self.add_circuit('right',
                         target=self.safe_legs.right,
                         pre=[move_synapse])
        self.add_circuit('stop', target=self.safe_legs.stop)
        self.add_circuit('set_speed',
                         target=self.safe_legs.set_speed,
                         pre=[speedvalue_synapse])
        self.add_circuit('set_movetime',
                         target=self.safe_legs.set_movetime,
                         pre=[movetime_synapse])

        self.add_circuit('say', target=self.safe_mouth.say, pre=[say_synapse])
        self.add_circuit('shutup', target=self.safe_mouth.shutup)

        self.add_circuit('open_eyes', target=self.safe_eye.open)
        self.add_circuit('close_eyes', target=self.safe_eye.close)

    def add_circuit(self, name, target, pre=None, post=None):
        """Method to add a new cirtcuit made by synapses.
        You have to give it a name and specify the target(aka core function)
        of the synapse. Optionally you can give functions which will be
        called before `target` and should take the same arguments of `target`
        and return a tuple of (args, kwargs). Moreover you can optionally give
        functions which will be called after `target` and they should take
        the result of `target`(or nothing if the function returns None).
        The returned value of the `post-workers` is ignored.

        Args:
            name (str): name of the circuit
            target (callable): core function to call
            pre (iterable of callables): pre-workers synapses called before `target`
            post (iterable of callables): post-workers synapses called after `target`
        """
        self.circuits[name] = {
            'pre-work': pre or [],
            'target': target,
            'post-work': post or []
        }


class Brain:
    """This is the logic part of the body.
    Basically it allows you to call a given synapse of a
    body by its name handling pre-workers and post-workers.
    """

    def __init__(self, body):
        """Creates a new Brain that handles a given Body.

        Args:
            body (Body): body object to manage
        """
        self.body = body

    def get_help(self):
        """Utility function that returns the docstring for each
        synapse.

        Returns:
            dict: a dictionary with the synapse name as the key and
                another dict as values containing only the docstring
                of the synapse. We return a dict as the value, because
                new features will be definitely added.
        """
        ret = {}
        for name in self.body.circuits:
            ret[name] = {'doc': self.body.circuits[name]['target'].__doc__}

        return ret

    def call(self, name, *args, **kwargs):
        """Executes the circuit identified by `name` with
        the given arguments.

        Args:
            name (str): name of the circuit
            args: argument list to pass to pre-workers and target
            kwargs: keyword arguments to pass to pre-workers and target

        Returns:
            Whatever 'target' returns.
        """
        syn = self.body.circuits[name]
        for p in syn['pre-work']:
            args, kwargs = p(*args, **kwargs)
        r = syn['target'](*args, **kwargs)
        for p in syn['post-work']:
            p(r) if r else p()
        return r
