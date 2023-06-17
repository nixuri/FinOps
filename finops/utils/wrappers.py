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

def catch(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            result = None
        return result

    return wrapper