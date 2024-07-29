import time
import subprocess

def is_screen_on():
    result = subprocess.run(['adb', 'shell', 'dumpsys', 'power'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    if 'mHoldingDisplaySuspendBlocker=true' in output or 'Display Power: state=ON' in output:
        return True
    else:
        return False

def run_command(command):
    # windows
    subprocess.run(command, shell=True, text=True)
    # linux - termux
    # subprocess.run(command + " > /dev/null 2>&1", shell=True, text=True)

if __name__ == '__main__':
    print("Begin at: {}".format(time.strftime("%H:%M:%S", time.localtime())))

    # efastefree_cnt = 0
    # cryptowin_cnt = 0

    while True:
        #if not is_screen_on():
            #subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_POWER'])
        
        run_command('python -u ./cryptorize/main.py')

        '''
        begin_time_efastefree = time.time()
        run_command("python -u ./efastefree/main.py")
        if time.time() - begin_time_efastefree > 30 * 60:
            print("------------------------")
            print(f"efastefree cost: {(time.time() - begin_time_efastefree) / 60.0} minutes")
            efastefree_cnt = efastefree_cnt + 1
            print("Running count efastefree =", efastefree_cnt)
        '''

        '''
        begin_time_cryptowin = time.time()
        run_command("python -u ./cryptowin/main.py")
        if time.time() - begin_time_cryptowin > 15 * 60:
            print("------------------------")
            print(f"cryptowin cost: {(time.time() - begin_time_cryptowin) / 60.0} minutes")
            cryptowin_cnt = cryptowin_cnt + 1
            print("Running count cryptowin =", cryptowin_cnt)
        '''

        # subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_POWER'])
        
