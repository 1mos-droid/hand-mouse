import mediapipe
import sys
import os

print("--- DIAGNOSTIC REPORT ---")
print(f"Python Version: {sys.version.split()[0]}")
try:
    print(f"MediaPipe Location: {mediapipe.__file__}")
except AttributeError:
    print("MediaPipe Location: (It is a folder/namespace package)")
    if hasattr(mediapipe, '__path__'):
         print(f"Folder Path: {list(mediapipe.__path__)}")

print(f"Current Working Directory: {os.getcwd()}")
print("-------------------------")