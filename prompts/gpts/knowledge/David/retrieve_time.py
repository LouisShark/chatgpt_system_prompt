
def retrieve_time():
    with open('time_tracker.txt', 'r') as file:
        last_updated_time = file.read()
    return last_updated_time


if __name__ == "__main__":
    print(retrieve_time())
