import time
import random
import win32gui
import win32con
import re
import psutil
import keyboard
from pywinauto.keyboard import send_keys

def log_action(action, status):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} - {action} - {status}"
    print(log)  # Print to console
    with open("log.txt", "a") as f:
        f.write(log + "\n")  # Write to log file

def extract_coordinates(text):
    match = re.search(r"x:(-?\d+\.\d+)\s+y:(-?\d+\.\d+)\s+z:(-?\d+\.\d+)", text)
    if match:
        x = match.group(1)
        y = match.group(2)
        z = match.group(3)
        return f"Coordinates: x:{x} y:{y} z:{z}"
    return None

def get_window_state(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    return placement[1]

def set_window_state(hwnd, state):
    placement = win32gui.GetWindowPlacement(hwnd)
    placement[1] = state
    win32gui.SetWindowPlacement(hwnd, placement)

def check_starcitizen():
    try:
        starcitizen_hwnd = win32gui.FindWindow(None, "Star Citizen")
        if starcitizen_hwnd != 0:
            # Check if Star Citizen is a live process
            starcitizen_pid = None
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == "StarCitizen.exe":
                    starcitizen_pid = proc.info['pid']
                    break
            if starcitizen_pid is not None:
                # Check if Star Citizen window is active
                active_hwnd = win32gui.GetForegroundWindow()
                if active_hwnd != starcitizen_hwnd:
                    # Store the current active window state
                    prev_hwnd = win32gui.GetForegroundWindow()
                    prev_state = get_window_state(prev_hwnd)

                    # Activate Star Citizen window
                    win32gui.ShowWindow(starcitizen_hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(starcitizen_hwnd)
                    time.sleep(0.1)

                    # Send keys to Star Citizen
                    send_keys("{F12}")
                    time.sleep(0.5)
                    send_keys("{F12}")

                    # Return to the previous active window
                    win32gui.ShowWindow(prev_hwnd, prev_state)
                    win32gui.SetForegroundWindow(prev_hwnd)
                    log_action("Star Citizen actions executed", "Success")

                else:
                    log_action("Star Citizen is already active", "Info")
            else:
                log_action("Star Citizen is not a live process", "Failed")
        else:
            log_action("Star Citizen window not found", "Failed")
    except Exception as e:
        log_action(f"An error occurred: {str(e)}", "Failed")

# Manual function to check clipboard for coordinates and log them
def check_clipboard():
    clipboard_text = send_keys("^v")
    coordinates = extract_coordinates(clipboard_text)
    if coordinates:
        log_action(coordinates, "Info")

# Main loop
import time
import random
import win32gui
import win32con
import re
import psutil
from pywinauto.keyboard import send_keys

def log_action(action, status):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} - {action} - {status}"
    print(log)  # Print to console
    with open("log.txt", "a") as f:
        f.write(log + "\n")  # Write to log file

def extract_coordinates(text):
    match = re.search(r"x:(-?\d+\.\d+)\s+y:(-?\d+\.\d+)\s+z:(-?\d+\.\d+)", text)
    if match:
        x = match.group(1)
        y = match.group(2)
        z = match.group(3)
        return f"Coordinates: x:{x} y:{y} z:{z}"
    return None

def get_window_state(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    return placement[1]

def set_window_state(hwnd, state):
    placement = win32gui.GetWindowPlacement(hwnd)
    placement[1] = state
    win32gui.SetWindowPlacement(hwnd, placement)

def check_starcitizen():
    try:
        starcitizen_hwnd = win32gui.FindWindow(None, "Star Citizen")
        if starcitizen_hwnd != 0:
            # Check if Star Citizen is a live process
            starcitizen_pid = None
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == "StarCitizen.exe":
                    starcitizen_pid = proc.info['pid']
                    break
            if starcitizen_pid is not None:
                # Check if Star Citizen window is active
                active_hwnd = win32gui.GetForegroundWindow()
                if active_hwnd != starcitizen_hwnd:
                    # Store the current active window state
                    prev_hwnd = win32gui.GetForegroundWindow()
                    prev_state = get_window_state(prev_hwnd)

                    # Activate Star Citizen window
                    win32gui.ShowWindow(starcitizen_hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(starcitizen_hwnd)
                    time.sleep(0.1)

                    # Send keys to Star Citizen
                    send_keys("{F12}")
                    time.sleep(0.1)
                    send_keys("{F12}")

                    # Return to the previous active window
                    win32gui.ShowWindow(prev_hwnd, prev_state)
                    win32gui.SetForegroundWindow(prev_hwnd)
                    log_action("Star Citizen actions executed", "Success")

                else:
                    log_action("Star Citizen is already active", "Info")
            else:
                log_action("Star Citizen is not a live process", "Failed")
        else:
            log_action("Star Citizen window not found", "Failed")
    except Exception as e:
        log_action(f"An error occurred: {str(e)}", "Failed")

def check_clipboard():
    clipboard_text = send_keys("^v")
    coordinates = extract_coordinates(clipboard_text)
    if coordinates:
        log_action(coordinates, "Info")

def manual_key_check():
    # Check if the LCtrl and RAlt keys are pressed
    if keyboard.is_pressed('left ctrl') and keyboard.is_pressed('right alt'):
        return True
    return False

# Main loop
manual_location_triggered = False
while True:
    # Random timer between 3 and 8 minutes
    random_timer = random.randint(180, 480)
    log_action("Checking Star Citizen status", "Info")
    check_starcitizen()

    if manual_key_check():
        manual_location_triggered = True
        log_action("Manual key combination triggered", "Success")

    if manual_location_triggered:
        manual_location_triggered = False

        # Send /showlocation manually
        send_keys("/showlocation")
        time.sleep(0.5)
        send_keys("{ENTER}")
        time.sleep(0.5)
        send_keys("{F12}")

        # Wait for coordinates to be copied to clipboard
        time.sleep(0.25)
        check_clipboard()
        log_action("Manual /showlocation executed", "Success")

    time.sleep(random_timer)

    
