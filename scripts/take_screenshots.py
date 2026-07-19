import os
import time
from playwright.sync_api import sync_playwright

output_dir = r"d:\Campus Core\current Ui"
os.makedirs(output_dir, exist_ok=True)

def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Go to home / login
        page.goto("http://localhost:5000/")
        time.sleep(2)
        page.screenshot(path=os.path.join(output_dir, "1_login_page.png"))
        
        # Login as Admin
        page.fill("input[name='email']", "admin@sist.ac.in")
        page.fill("input[name='password']", "admin123")
        page.click("button[type='submit']")
        time.sleep(3)
        page.screenshot(path=os.path.join(output_dir, "2_admin_dashboard.png"))
        
        # Navigate to a couple of admin pages
        page.goto("http://localhost:5000/admin/events")
        time.sleep(2)
        page.screenshot(path=os.path.join(output_dir, "3_admin_events.png"))
        
        # Logout
        page.goto("http://localhost:5000/logout")
        time.sleep(2)
        
        # Login as Organizer
        page.fill("input[name='email']", "organizer@sist.ac.in")
        page.fill("input[name='password']", "organizer123")
        page.click("button[type='submit']")
        time.sleep(3)
        page.screenshot(path=os.path.join(output_dir, "4_organizer_dashboard.png"))
        
        # Logout
        page.goto("http://localhost:5000/logout")
        time.sleep(2)
        
        # Login as Student
        page.fill("input[name='email']", "student@sist.ac.in")
        page.fill("input[name='password']", "student123")
        page.click("button[type='submit']")
        time.sleep(3)
        page.screenshot(path=os.path.join(output_dir, "5_student_dashboard.png"))
        
        # Go to events list for student
        page.goto("http://localhost:5000/student/events")
        time.sleep(2)
        page.screenshot(path=os.path.join(output_dir, "6_student_events.png"))

        browser.close()

if __name__ == "__main__":
    take_screenshots()
    print("Screenshots taken successfully!")
