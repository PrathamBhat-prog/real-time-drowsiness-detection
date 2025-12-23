from multiprocessing import Value
from ctypes import c_double, c_bool

ear_value = Value(c_double, 0.0)
is_drowsy = Value(c_bool, False)
