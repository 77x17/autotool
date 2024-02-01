import cv2
import time
import subprocess
from PIL import Image
  
run    = True
n_ok   = 0
N_EXIT = 8

def run_command(command):
    # windows
    # subprocess.run(command + " > NUL", shell=True, text=True)
    # linux - termux
    subprocess.run(command + " > /dev/null 2>&1", shell=True, text=True)

def take_screenshot(width = 1080, height = 1920):
    run_command("adb shell screencap /sdcard/Pictures/screenshot.raw && adb pull /sdcard/Pictures/screenshot.raw efastefree/screenshot.raw")
   
    bytespp = 4

    with open('efastefree/screenshot.raw', 'rb') as file:
        raw_data = file.read(width * height * bytespp)

    img_bytes = bytearray(raw_data)

    img = Image.frombytes('RGBA', (width, height), bytes(img_bytes), 'raw')

    img.save('efastefree/screenshot.png', 'PNG')

def findLocation(input_png, click = True):
    img_rgb  = cv2.imread('efastefree/screenshot.png')
    template = cv2.imread('efastefree/' + input_png)

    img_rgb  = cv2.resize(img_rgb,  (0, 0), fx=0.5, fy=0.5)
    template = cv2.resize(template, (0, 0), fx=0.5, fy=0.5)

    res       = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8

    if input_png[0:4] == 'exit':
        threshold = .65

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
 
    if max_val >= threshold:
        x, y = max_loc

        if click:            
            run_command(f"adb shell input tap {2 * x + template.shape[1]} {2 * y + template.shape[0]}")
            # print(input_png)
            # print(2 * x + template.shape[1], 2 * y + template.shape[0])
            
        return True

    return False

def efast_efree(start_time):
    global n_ok
    global run

    if n_ok == 10:
        run = False
        return    
    
    take_screenshot()

    # print("go")
    if findLocation("go.png"):
        time.sleep(1)
        take_screenshot()

        start_time[0] = time.time()
        
    # print("ok")
    if findLocation("ok.png", False):
        if findLocation("limit.png"):
            run = False

        findLocation("ok.png")

        n_ok = n_ok + 1
        start_time[0] = time.time()
        
        return
    
    # print("internet connection")
    while findLocation("retry.png"):
        time.sleep(1)
        take_screenshot()

        if findLocation("retry.png", False):
            time.sleep(300)

        start_time[0] = time.time()

    # print("equation")
    while findLocation("equation.png", False):
        ans = 0

        find = False
        for i in range(0, 5):
            if findLocation(f"numleft_{i}.png", False):
                ans += i
                find = True
                break

        if not find:
            ans = 9
        else:
            for i in range(0, 5):
                if findLocation(f"numright_{i}.png", False):
                    ans += i
                    find = True
                    break

            if not find:
                ans = 9

        findLocation("ansbox.png")

        run_command(f"adb shell input text {ans}")

        run_command("adb shell input keyevent 4")

        findLocation("equation.png")

        time.sleep(1)
        take_screenshot()

        start_time[0] = time.time()

    # print("ads")
    
    if findLocation("googleplay.png", False):
        run_command("adb shell input keyevent 4")
            
        time.sleep(1)
        take_screenshot()
        
    click = False

    for i in range(0, N_EXIT):
        if findLocation(f"exit_{i}.png"):
            time.sleep(1)
            take_screenshot()
            click = True

    if click:
        n_ok = 0
        return

    take_screenshot(1920, 1080)

    for i in range(0, N_EXIT):
        if findLocation(f"exit_{i}.png"):
            time.sleep(1)
            take_screenshot(1920, 1080)
            n_ok = 0

    if (time.time() - start_time[0]) > 180:
        n_ok = 0
        start_time[0] = time.time()
        run_command("adb shell am force-stop com.efast.efree")
        run_command("adb shell monkey -p com.efast.efree -c android.intent.category.LAUNCHER 1")

if __name__ == '__main__':
    run_command("adb shell monkey -p com.efast.efree -c android.intent.category.LAUNCHER 1")
    
    run = True

    start_time = [time.time()]
    while run:
        efast_efree(start_time)   
    
    run_command("adb shell am force-stop com.efast.efree")