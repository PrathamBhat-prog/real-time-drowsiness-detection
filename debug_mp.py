import sys
print(f"Python Version: {sys.version}")
print(f"Sys Path: {sys.path}")

try:
    import mediapipe as mp
    print(f"MediaPipe Version: {mp.__version__}")
    print(f"File: {mp.__file__}")
    
    if hasattr(mp, 'solutions'):
        print("mp.solutions exists!")
        print(f"Solutions: {mp.solutions}")
    else:
        print("mp.solutions is MISSING")
        
    try:
        import mediapipe.python.solutions as solutions
        print("Imported mediapipe.python.solutions successfully")
    except ImportError as ie:
        pass
        
except Exception as e:
    print(f"Error: {e}")
