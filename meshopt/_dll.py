"""meshoptimzer DLL loader"""

import os
from ctypes import cdll


meshoptdll = cdll.LoadLibrary(
    os.path.join(os.path.dirname(__file__), 'meshoptimizer.dll')
)

del os
del cdll
