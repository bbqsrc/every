# Every

Run a method at a set interval.

## Usage

```python
from every import run
import time

def foo():
    print(time.time())

# Run method every 5 seconds
x = run(foo).every(5, 'seconds')

# Run method every 1 minute, not running method immediately
y = run(foo).every(1, 'minutes', immediate=False)

time.sleep(20)

# .join() will set the looping flag to False and cause the thread to end
x.join()

# .join(stop=False) works like an ordinary thread: wait until thread finishes, then end
y.join(stop=False)
```

## License

Creative Commons Zero
