import time
import threading

g_import_finished = False


def __loading_bar():
    animation = [
        "[        ]",
        "[=       ]",
        "[===     ]",
        "[====    ]",
        "[=====   ]",
        "[======  ]",
        "[======= ]",
        "[========]",
        "[ =======]",
        "[  ======]",
        "[   =====]",
        "[    ====]",
        "[     ===]",
        "[      ==]",
        "[       =]",
        "[        ]",
        "[        ]",
    ]

    i = 0
    print("Getting Julia ready...")
    t = time.time()
    while not g_import_finished:
        if time.time() - t > 100:
            exit("ErrorCritical: Timeout")
        print(animation[i % len(animation)] + "\r")
        time.sleep(0.1)
        i += 1


def loading_bar_handler(loading_is_finished):
    global loading_thread
    if not loading_is_finished:
        loading_thread = threading.Thread(target=__loading_bar)
        loading_thread.start()
    else:
        global g_import_finished
        g_import_finished = loading_is_finished
        print("Julia is ready")
        loading_thread.join()
