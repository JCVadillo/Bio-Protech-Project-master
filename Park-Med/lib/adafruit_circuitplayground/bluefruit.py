# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, bluefruit OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_circuitplayground.bluefruit`
====================================================

CircuitPython helper for Circuit Playground Bluefruit.

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Circuit Playground Bluefruit <https://www.adafruit.com/product/4333>`_

"""

import array
import math
import digitalio
import board
import audiopwmio
import audiobusio
from adafruit_circuitplayground.circuit_playground_base import CircuitPlaygroundBase


__version__ = "4.0.2"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Bluefruit(CircuitPlaygroundBase):
    """Represents a single CircuitPlayground Bluefruit."""

    _audio_out = audiopwmio.PWMAudioOut

    def __init__(self):
        # Only create the cpb module member when we aren't being imported by Sphinx
        if ("__module__" in dir(digitalio.DigitalInOut) and
                digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"):
            return

        super().__init__()

        self._sample = None

        # Define mic/sound sensor:
        self._mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                                     sample_rate=16000, bit_depth=16)
        self._samples = None

    @staticmethod
    def _normalized_rms(values):
        mean_values = int(sum(values) / len(values))
        return math.sqrt(sum(float(sample - mean_values) * (sample - mean_values)
                             for sample in values) / len(values))

    @property
    def sound_level(self):
        """Obtain the sound level from the microphone (sound sensor).

        .. image :: ../docs/_static/microphone.jpg
          :alt: Microphone (sound sensor)

        This example prints the sound levels. Try clapping or blowing on
        the microphone to see the levels change.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              print(cpb.sound_level)
        """
        if self._sample is None:
            self._samples = array.array('H', [0] * 160)
        self._mic.record(self._samples, len(self._samples))
        return self._normalized_rms(self._samples)

    def loud_sound(self, sound_threshold=200):
        """Utilise a loud sound as an input.

        :param int sound_threshold: Threshold sound level must exceed to return true (Default: 200)

        .. image :: ../docs/_static/microphone.jpg
          :alt: Microphone (sound sensor)

        This example turns the LEDs red each time you make a loud sound.
        Try clapping or blowing onto the microphone to trigger it.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              if cpb.loud_sound():
                  cpb.pixels.fill((50, 0, 0))
              else:
                  cpb.pixels.fill(0)

        You may find that the code is not responding how you would like.
        If this is the case, you can change the loud sound threshold to
        make it more or less responsive. Setting it to a higher number
        means it will take a louder sound to trigger. Setting it to a
        lower number will take a quieter sound to trigger. The following
        example shows the threshold being set to a higher number than
        the default.

        .. code-block:: python

          from adafruit_circuitplayground.bluefruit import cpb

          while True:
              if cpb.loud_sound(sound_threshold=300):
                  cpb.pixels.fill((50, 0, 0))
              else:
                  cpb.pixels.fill(0)
        """

        return self.sound_level > sound_threshold


cpb = Bluefruit()  # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.bluefruit import cpb
"""
