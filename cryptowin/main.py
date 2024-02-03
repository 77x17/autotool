import cv2
import time
import subprocess
from PIL import Image
  
run    = True
n_ok   = 0
N_EXIT = 6

def run_command(command):
    # windows
    # subprocess.run(command + " > NUL", shell=True, text=True)
    # linux - termux
    subprocess.run(command + " > /dev/null 2>&1", shell=True, text=True)

def take_screenshot(width = 1080, height = 1920):
    run_command("adb shell screencap /sdcard/Pictures/screenshot.raw && adb pull /sdcard/Pictures/screenshot.raw cryptowin/screenshot.raw")
   
    bytespp = 4

    with open('cryptowin/screenshot.raw', 'rb') as file:
        raw_data = file.read(width * height * bytespp)

    img_bytes = bytearray(raw_data)

    img = Image.frombytes('RGBA', (width, height), bytes(img_bytes), 'raw')

    img.save('cryptowin/screenshot.png', 'PNG')

def findLocation(input_png, click = True, from_x = 0, from_y = 0, to_x = 1080, to_y = 1920):
    img_rgb  = cv2.imread('cryptowin/screenshot.png')
    img_rgb  = img_rgb[from_y:to_y, from_x:to_x]
    template = cv2.imread('cryptowin/' + input_png)

    # img_rgb  = cv2.resize(img_rgb,  (0, 0), fx=0.5, fy=0.5)
    # template = cv2.resize(template, (0, 0), fx=0.5, fy=0.5)

    res       = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8

    if input_png[0:4] == 'exit':
        threshold = .65

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
 
    if max_val >= threshold:
        x, y = max_loc

        if click:            
            # run_command(f"adb shell input tap {2 * x + template.shape[1]} {2 * y + template.shape[0]}")
            run_command(f"adb shell input tap {x + template.shape[1] / 2} {y + template.shape[0] / 2}")
            # print(input_png)
            # print(x + template.shape[1] / 2, y + template.shape[0] / 2)
        return True

    return False

def cryptoWin(start_time):
    global n_ok
    global run
    take_screenshot()

    # print('play')
    if findLocation('playbutton.png'):
        time.sleep(1)
        take_screenshot()

        start_time[0] = time.time()

    # print('ok')
    if findLocation("ok.png", False):
        if findLocation("limit.png"):
            run = False

        if n_ok == 10:
            run = False

        findLocation("ok.png")

        n_ok = n_ok + 1
        start_time[0] = time.time()

        return

    # print('exit ads')
    if findLocation("googleplay.png", False):
        run_command("adb shell input keyevent 4")
            
        time.sleep(1)
        take_screenshot()
    
    for i in range(0, N_EXIT):
        if findLocation(f"exit_{i}.png"):
            n_ok = 0
            time.sleep(1)
            take_screenshot()

    # print('ingame')
    if findLocation('ingame.png', False):
        take_screenshot()

        # print('begin calc')
        gem_type = [[0] * 4 for i in range(4)]

        for i in range(0, 4):
            for j in range(0, 4):
                run_command(f'adb shell input tap {135 + i * 270} {600 + j * 260}')
                take_screenshot()

                for x in range(1, 9):
                    if findLocation(f'gem_{x}.png', False, i * 270, 465 + j * 260, (i + 1) * 270, 465 + (j + 1) * 260):
                        gem_type[i][j] = x
                        break

        for x in range(1, 9):
            for i in range(0, 4):
                for j in range(0, 4):
                    if gem_type[i][j] == x:
                        run_command(f'adb shell input tap {135 + i * 270} {600 + j * 260}')
    
        start_time[0] = time.time()

        while not findLocation('next.png'):
            time.sleep(1)
            take_screenshot()

            if (time.time() - start_time[0]) > 30:
                n_ok = 0
                start_time[0] = time.time()
                run_command("adb shell am force-stop com.bprogrammers.cryptowin")
                run_command("adb shell monkey -p com.bprogrammers.cryptowin -c android.intent.category.LAUNCHER 1")

                return

        start_time[0] = time.time()

        run_command("adb shell am force-stop com.bprogrammers.cryptowin")
        run_command("adb shell monkey -p com.bprogrammers.cryptowin -c android.intent.category.LAUNCHER 1")

    if (time.time() - start_time[0]) > 180:
        n_ok = 0
        start_time[0] = time.time()
        run_command("adb shell am force-stop com.bprogrammers.cryptowin")
        run_command("adb shell monkey -p com.bprogrammers.cryptowin -c android.intent.category.LAUNCHER 1")

if __name__ == '__main__':
    run_command("adb shell monkey -p com.bprogrammers.cryptowin -c android.intent.category.LAUNCHER 1")

    run = True

    start_time = [time.time()]
    while run:
        cryptoWin(start_time)

    run_command("adb shell am force-stop com.bprogrammers.cryptowin")