"""This module contains the mouth that
the rover will use to make some noise.
By default it uses as backend `espeak` but it should
be easy to switch to `festival` or similar.
"""

from queue import Queue

import threading
import subprocess

from util import XMException


class UnableToSay(XMException):
    """Exception raised if you want to add a new sentence
    to the mouth queue that has been shut down.
    """
    pass


class Mouth:
    """Manager of a queue of sententeces to pronounce.
    Sentences are stored in thread safe queue that a working
    thread will use to retrieve the current sentence and play it.

    To add a new sentence to the queue just call `say` and pass the
    given sentence. If you want to stop the working thread (therefore
    it will not speak anymore) call `shutup`.

    Example:
        mouth = Mouth()

        mouth.say(Sentence('Hello I am XM'))
        mouth.say(Sentence('Amplitude increased', amplitude=150))
        mouth.say(Sentence('Talking very slow', wpm=1))

        import time
        time.sleep(5)

        mouth.shutup()
    """

    def __init__(self):
        """Default constructor
        """
        self.sentences = Queue()
        self.stop_speaking = threading.Event()
        thread = threading.Thread(target=process_sentences,
                                  args=(self.stop_speaking, self.sentences))
        thread.start()

    def say(self, text, amplitude=40, wpm=130, prog='espeak'):
        """Creates a new Sentence that when played will say `text`
        with a given `amplitude` and words per minute.
        By default the program that will be used to process the sentences
        is `espeak` but it should be possible to call it with `festival`.

        Args:
            text (str): text to say
            prog (str, optional): backend program that will actually say the text
            amplitude (int, optional): amplitude level of the sentence
            wpm (int, optional): words per minute(aka speed) to pronounce

        Raises:
            UnableToSay: if the mouth has been shut down
        """
        if self.stop_speaking.is_set():
            raise UnableToSay('''Mouth has been shut down.
                You can' t add a new sentence, it will not be played''')
        self.sentences.put(Sentence(text, prog, amplitude, wpm))

    def shutup(self):
        """Close the mouth.
        If you close the mouth you will be unable to play new sentences on it.
        """
        self.stop_speaking.set()
        self.sentences.put(None)  # just to wake up working thread if waiting


def process_sentences(stop_speaking, sentences):
    """Function the working thread will use to process sentences.

    Args:
        stop_speaking (threading.Event): flag used to check it the
            thread should stop
        sentences (iterable of Sentence): sentences to play
    """
    while not stop_speaking.is_set():
        snt = sentences.get()
        if snt:
            snt.play()
            sentences.task_done()


class Sentence:
    """This is a single sentence that a mouth will play.
    Every sentence has its own backend and a couple of util options.
    """

    def __init__(self, text, prog, amplitude, wpm):
        """Creates a new Sentence that when played will say `text`
        with a given `amplitude` and words per minute.

        Args:
            text (str): text to say
            prog (str): backend program that will actually say the text
            amplitude (int): amplitude level of the sentence
            wpm (int): words per minute(aka speed) to pronounce
        """
        self.text = text
        self.amplitude = amplitude
        self.wpm = wpm
        self.prog = prog

    def play(self):
        """Calls the backend with the amplitude and words per minute
        options.

        Returns:
            int: the return code of the backend
        """
        amp = '-a {:d}'.format(self.amplitude)
        wpm = '-s {:d}'.format(self.wpm)
        return subprocess.call([self.prog, amp, wpm, self.text])


if __name__ == '__main__':
    mouth = Mouth()

    mouth.say('Hello I am XM')
    mouth.say('Amplitude increased', amplitude=150)
    mouth.say('Talking very slow', wpm=1)

    import time
    time.sleep(5)

    mouth.shutup()
