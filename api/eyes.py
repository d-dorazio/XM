"""This module provides control on the streaming backend.
In particular it uses `mjpg-streamer` as its backend because
it's lightweight and it has good performance.
"""

import subprocess


class Eyes:
    """Class that manages the opening and closing of the
    backend. A bunch of options are available for istance you
    can set the path for the binary, the resolution, port, etc...
    To start the backend call `open` and to close it call `close`.
    """

    def __init__(self,
                 mjpg_streamer='mjpg_streamer',
                 log=None,
                 in_lib='/usr/local/lib/input_uvc.so',
                 out_lib='/usr/local/lib/output_http.so',
                 dev='/dev/video0',
                 framerate=5,
                 resolution=(320, 240),
                 commands=False,
                 yuv=True,
                 port=8090,
                 www='/usr/local/www'):
        """Creates a new manager for the streaming backend.

        Args:
            mjpg_streamer(str, optional): path for the `mjpg-streamer` binary.
                The default is 'mjpg_streamer'.
            log(file-like object, optional): optional file like object
                where to store the output of the backend.
                By default it's stdout.
            in_lib(str, optional): library to use to get the input from the
                camera. By default it is '/usr/local/lib/input_uvc.so'.
            out_lib(str, optional): library to use to stream over http. By
                default it's '/usr/local/lib/output_http.so'.
            dev(str, optional): the device to get video from. By default it's
                '/dev/video0'.
            framerate(int, optional): frames per second, by default it's 5.
            resolution((int, int), optional): resolution of the stream. It's a
                tuple of widthxheight integers.
            commands(bool, optional): whether to use commands or not. By defaul
                it's False.
            yuv(bool, optional): whether to use YUV format or not. By default
                it's True.
            port(int, optional): which port to stream on. By default it's 8090.
            www(str, optional): path where to store images and backup stuff.
                By default it's '/usr/local/www'.
        """
        self.mjpg_streamer = mjpg_streamer
        self.log = log
        self.in_lib = in_lib
        self.out_lib = out_lib
        self.dev = dev
        self.framerate = framerate
        self.resolution = resolution
        self.commands = commands
        self.yuv = yuv
        self.port = port
        self.www = www
        self._process = None

    def open(self):
        """Creates the backend process and starts streaming. If the backend
        is already open, then no action will be performed.
        """
        if self._process:
            return

        in_dev = '{ind} -d {dev} {cmd} {yuv} -r {res} -f {fps}'.format(
            ind=self.in_lib,
            dev=self.dev,
            cmd='' if self.commands else '-n',
            yuv='-y' if self.yuv else '',
            res='{:d}x{:d}'.format(*self.resolution),
            fps=self.framerate)
        out_dev = '{out} -p {port:d} -w {www}'.format(out=self.out_lib,
                                                      port=self.port,
                                                      www=self.www)
        self._process = subprocess.Popen([self.mjpg_streamer, '-i', in_dev,
                                          '-o', out_dev],
                                         stdout=self.log, stderr=self.log)

    def close(self):
        """Kills the running backend process. If there is no running backend
        process, no actions will be performed.
        """
        if self._process:
            self._process.kill()
            self._process = None
