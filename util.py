def normalize_time(time: str) -> str:
    time = time[3:] if time.startswith("0:0") else time
    time = time[2:] if time.startswith("0:") else time
    return time[:-3] if "." in time else time
