import datetime
from datetime import date
import time

current_time = time.time()
readable = time.ctime(current_time)
print("Readable time:", readable)