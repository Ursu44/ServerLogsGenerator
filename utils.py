import random
import time
from datetime import datetime, timezone

_attack_wave = False
_wave_counter = 0
_WAVE_LENGTH = 8
_CALM_LENGTH = 15

def is_attack_wave():
    global _attack_wave, _wave_counter
    _wave_counter += 1
    if _attack_wave and _wave_counter >= _WAVE_LENGTH:
        _attack_wave = False
        _wave_counter = 0
    elif not _attack_wave and _wave_counter >= _CALM_LENGTH:
        _attack_wave = True
        _wave_counter = 0
    return _attack_wave

def random_ip():
    private_ranges = [
        lambda: f"172.{random.randint(16,27)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    ]
    public_ranges = [
        lambda: f"31.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"52.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
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