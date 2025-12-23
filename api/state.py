from multiprocessing import Value
from ctypes import c_double, c_bool, c_char_p

# Shared Values (Thread-safe/Process-safe primitive wrappers)
ear_value = Value(c_double, 0.0)
is_drowsy = Value(c_bool, False)
attention_state = Value(c_char_p, b"UNKNOWN")

# For threaded mode, a simple dict is sufficient.
# Warning: This is NOT process-safe if you switch back to multiprocessing.Process!
metrics_snapshot = {} 
