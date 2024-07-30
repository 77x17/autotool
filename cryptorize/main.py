import cv2
import time
import subprocess
from PIL import Image

N_SKIP = 1
N_EXIT = 1

def run_command(command):
    # windows
    # subprocess.run(command + " > NUL", shell=True, text=True)
    # linux - termux
    subprocess.run(command + " > /dev/null 2>&1", shell=True, text=True)

def take_screenshot(width = 1080, height = 1920):
    run_command("adb shell screencap /sdcard/Pictures/screenshot.raw && adb pull /sdcard/Pictures/screenshot.raw cryptorize/screenshot.raw")
   
    bytespp = 4

    with open('cryptorize/screenshot.raw', 'rb') as file:
        raw_data = file.read(width * height * bytespp)

    img_bytes = bytearray(raw_data)

    img = Image.frombytes('RGBA', (width, height), bytes(img_bytes), 'raw')

    img.save('cryptorize/screenshot.png', 'PNG')

def findLocation(input_png, click = True, from_x = 0, from_y = 0, to_x = 1080, to_y = 1920):
    img_rgb  = cv2.imread('cryptorize/screenshot.png')
    img_rgb  = img_rgb[from_y:to_y, from_x:to_x]
    template = cv2.imread('cryptorize/' + input_png)

    res       = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .65

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
 
    if max_val >= threshold:
        x, y = max_loc

        if click:            
            run_command(f"adb shell input tap {x + template.shape[1] / 2} {y + template.shape[0] / 2}")
            # print(input_png)
            # print(x + template.shape[1] / 2, y + template.shape[0] / 2)
        return True

    return False

def CryptoRize(start_time):
    take_screenshot()

    if findLocation('ok.png'):
        #print('ok')
        time.sleep(3)
        take_screenshot()

    if findLocation('playbutton.png'):
        #print('playbutton')
        time.sleep(15)
        take_screenshot()

    for i in range(0, N_SKIP):
        if findLocation(f'skip_{i}.png'):
            #print('skip ads')
            time.sleep(5)
            take_screenshot()

    for i in range(0, N_EXIT):
        if findLocation(f'exit_{i}.png'):
            #print('exit ads')
            time.sleep(5)
            take_screenshot()

    if findLocation('ingame.png', False):
        stop = 0
        #print('ingame')
        while stop != -1 and time.time() - start_time[0] < 600: 
            if stop % 2 == 0:
                run_command('adb shell input swipe 540 1400 540 200')
            else:
                run_command('adb shell input swipe 540 600 540 1900')
            stop = stop + 1

            for i in range(0, 6):
                if 2 <= i and i <= 3:
                    for j in range(0, 5):
                        run_command(f'adb shell input tap {170 + i * 150} {600 + j * 150}')
                    
                    time.sleep(5)
                    take_screenshot()
                    if findLocation('completed.png', False):
                        i = 6
                        stop = -1
                        break
                    else:
                        run_command(f'adb shell input tap {170 + i * 150} {600 + 5 * 150}')
                else:
                    for j in range(0, 6):
                        run_command(f'adb shell input tap {170 + i * 150} {600 + j * 150}')

        run_command('adb shell am force-stop com.bprogrammers.cryptorize')
        run_command('adb shell monkey -p com.bprogrammers.cryptorize -c android.intent.category.LAUNCHER 1')
        
        #print(time.time() - start_time[0])
        start_time[0] = time.time()
        
    if time.time() - start_time[0] > 600:
        run_command('adb shell am force-stop com.bprogrammers.cryptorize')
        run_command('adb shell monkey -p com.bprogrammers.cryptorize -c android.intent.category.LAUNCHER 1')
        start_time[0] = time.time()

if __name__ == '__main__':
    run_command('adb shell monkey -p com.bprogrammers.cryptorize -c android.intent.category.LAUNCHER 1')

    start_time = [time.time()]
    while True:
        CryptoRize(start_time)