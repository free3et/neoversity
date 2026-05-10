def caching_fibonacci():
    cache = {} # cache for storing the results of the fibonacci sequence

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache: # if the result is already in the cache, return it
            return cache[n]
        else: # if the result is not in the cache, calculate it and store it in the cache
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    return fibonacci # return the function itself
    
fib = caching_fibonacci()
print(fib(10))
print(fib(15))
print(fib(50))
print(fib(200))
