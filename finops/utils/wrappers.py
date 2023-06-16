import threading

def lock(func):
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            result = func(*args, **kwargs)
        finally:
            lock.release()
        return result

    return wrapper