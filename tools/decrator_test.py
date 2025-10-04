from functools import wraps

def log_if(debug=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if debug:
                print(f"调用函数: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用
@log_if(debug=True)
def add(a, b):
    return a + b

add(3, 5)