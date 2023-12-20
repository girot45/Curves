import ctypes
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(current_dir, 'source_codes/maple.dll')

bigint_dll = ctypes.CDLL(dll_path)

gcd_ = bigint_dll.gcd
gcd_.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
gcd_.restype = ctypes.c_char_p

isprime_ = bigint_dll.isprime
isprime_.argtypes = [ctypes.c_char_p]
isprime_.restype = ctypes.c_bool

rem_ = bigint_dll.rem
rem_.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
rem_.restype = ctypes.c_char_p

phi_ = bigint_dll.phi
phi_.argtypes = [ctypes.c_char_p]
phi_.restype = ctypes.c_char_p