import datetime

def update_time():
    current_time = datetime.datetime.now().isoformat()
    with open('time_tracker.txt', 'w') as file:
        file.write(current_time)


if __name__ == "__main__":
    update_time()
