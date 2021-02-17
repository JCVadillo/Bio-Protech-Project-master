# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2017-2019 Kattni Rembor for Adafruit Industries
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_circuitplayground.express`
====================================================

CircuitPython helper for Circuit Playground Express.

**Hardware:**

* `Circuit Playground Express <https://www.adafruit.com/product/3333>`_

* Author(s): Kattni Rembor, Scott Shawcroft
"""

import sys
import audioio
import digitalio
# pylint: disable=wrong-import-position
try:
    lib_index = sys.path.index("/lib")        # pylint: disable=invalid-name
    if lib_index < sys.path.index(".frozen"):
        # Prefer frozen modules over those in /lib.
        sys.path.insert(lib_index, ".frozen")
except ValueError:
    # Don't change sys.path if it doesn't contain "lib" or ".frozen".
    pass
from adafruit_circuitplayground.circuit_playground_base import CircuitPlaygroundBase


__version__ = "4.0.2"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground.git"


class Express(CircuitPlaygroundBase):
    """Represents a single CircuitPlayground Express. Do not use more than one at
       a time."""

    # Touch pad A7 is labeled both A7/TX on Circuit Playground Express and only TX on
    # the Circuit Playground Bluefruit. It is therefore referred to as TX in the
    # CircuitPlaygroundBase class, but can be used as either for Express.
    touch_A7 = CircuitPlaygroundBase.touch_TX
    _audio_out = audioio.AudioOut

    def __init__(self):
        # Only create the cpx module member when we aren't being imported by Sphinx
        if ("__module__" in dir(digitalio.DigitalInOut) and
                digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"):
            return

        super().__init__()

    @property
    def _unsupported(self):
        """This feature is not supported on Circuit Playground Express."""
        raise NotImplementedError("This feature is not supported on Circuit Playground Express.")

    # The following is a list of the features available in other Circuit Playground modules but
    # not available for Circuit Playground Express. If called while using a Circuit Playground
    # Express, they will result in the NotImplementedError raised in the property above.
    sound_level = _unsupported
    loud_sound = _unsupported


cpx = Express()  # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_circuitplayground.express import cpx
"""
