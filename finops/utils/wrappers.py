import time

def catch(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            result = None
        return result

    return wrapper

def sleep(func):
    def wrapper(*args, **kwargs):
        time.sleep(1)
        result = func(*args, **kwargs)
        return result

    return wrapper

def retry(max_retries=3, wait_time=10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    retry_count += 1
                    print(f"Retrying - Attempt {retry_count} of {max_retries}")
        return wrapper
    return decorator