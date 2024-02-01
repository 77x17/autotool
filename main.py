import time
import subprocess

def run_command(command):
    # windows
    # subprocess.run(command, shell=True, text=True)
    # linux - termux
    subprocess.run(command + " > /dev/null 2>&1", shell=True, text=True)

if __name__ == '__main__':
    print("Begin at: {}".format(time.strftime("%H:%M:%S", time.localtime())))

    efastefree_cnt = 0
    cryptowin_cnt = 0

    while True:
        begin_time_efastefree = time.time()
        run_command("python -u ./efastefree/main.py")
        if time.time() - begin_time_efastefree > 30 * 60:
            print("------------------------")
            print(f"efastefree cost: {(time.time() - begin_time_efastefree) / 60.0} hours")
            efastefree_cnt = efastefree_cnt + 1
            print("Running count efastefree =", efastefree_cnt)

        begin_time_cryptowin = time.time()
        run_command("python -u ./cryptowin/main.py")
        if time.time() - begin_time_cryptowin > 15 * 60:
            print("------------------------")
            print(f"efastefree cost: {(time.time() - begin_time_cryptowin) / 60.0} hours")
            cryptowin_cnt = cryptowin_cnt + 1
            print("Running count efastefree =", cryptowin_cnt)
