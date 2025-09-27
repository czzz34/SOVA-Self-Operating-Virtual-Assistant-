# functions/libraries.py
import time
import threading
import logging
import json
import os
import base64
import random
import webbrowser
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
import ollama
import tkinter as tk
from tkinter import Text, filedialog, simpledialog, ttk
from PIL import Image, ImageTk
import pyautogui
import psutil
import pynvml
import wmi
import speech_recognition as sr
import pyttsx3

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
