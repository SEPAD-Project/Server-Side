import pyautogui
import time

# Disable fail-safe (optional)
pyautogui.FAILSAFE = False

def click_at_points(points):
    """
    Clicks on the specified points
    """
    for i, point in enumerate(points):
        print(f"Click {i+1} at position: {point}")
        pyautogui.click(point[0], point[1])
        time.sleep(1)  # Delay between clicks

def main():
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()
    print(f"Screen dimensions: {screen_width}x{screen_height}")
    
    # Calculate 3 points that divide the screen width into 3 equal parts
    # We'll click at the vertical center for each section
    section_width = screen_width // 3
    center_y = screen_height // 2
    
    points = [
        (section_width // 2, center_y),        # Center of first section
        (section_width + section_width // 2, center_y),  # Center of second section
        (2 * section_width + section_width // 2, center_y)  # Center of third section
    ]
    
    print("Auto-clicker started. Press Ctrl+C to stop.")
    print(f"Click points: {points}")
    
    try:
        while True:
            click_at_points(points)
            print("Waiting 30 seconds...")
            time.sleep(30)  # Wait 30 seconds
    except KeyboardInterrupt:
        print("\nClicker stopped.")

if __name__ == "__main__":
    main()