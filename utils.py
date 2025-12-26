import random
import time
from datetime import datetime,timezone

def random_ip():
    private_ranges = [
        lambda: f"172.{random.randint(16,27)}.{random.randint(0,25)}.{random.randint(1,25)}",
        lambda: f"192.168.{random.randint(0,25)}.{random.randint(1,25)}"
    ]

    public_ranges = [
        lambda: f"31.{random.randint(0,25)}.{random.randint(0,25)}.{random.randint(0,25)}",
        lambda: f"52.{random.randint(0,25)}.{random.randint(0,25)}.{random.randint(0,25)}"
    ]

    return random.choice(private_ranges + public_ranges)()

def random_user():
    users = [
        "admin", "root", "user1", "user2",
        "service", "backup", "test",
        "guest", "support"
    ]
    return random.choice(users)

def timestamp_syslog():
    return datetime.now(timezone.utc).strftime("%b %d %H:%M:%S")

def timestamp_epoch():
    return f"{time.time():.3f}"
