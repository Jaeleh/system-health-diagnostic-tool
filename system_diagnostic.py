import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime


def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    gb = 1024 ** 3
    percent_used = (used / total) * 100
    status = "WARNING: Low Disk Space" if percent_used > 85 else "OK"
    return (
        f"Total: {total / gb:.1f} GB | Free: {free / gb:.1f} GB "
        f"({percent_used:.1f}% used) -> [{status}]"
    )


def check_network(host="8.8.8.8"):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", host]
    result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return "PASS (Connected)" if result.returncode == 0 else "FAIL (No Connection)"


def check_dns(domain="google.com"):
    try:
        ip = socket.gethostbyname(domain)
        return f"PASS ({domain} resolved to {ip})"
    except socket.gaierror:
        return f"FAIL (Could not resolve {domain})"


def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    os_info = f"{platform.system()} {platform.release()}"

    report_lines = [
        "==========================================",
        "   AUTOMATED SYSTEM DIAGNOSTIC REPORT",
        "==========================================",
        f"Timestamp : {timestamp}",
        f"Host Name : {hostname}",
        f"OS Version: {os_info}",
        "------------------------------------------",
        f"Disk Health : {check_disk_space()}",
        f"Internet    : {check_network()}",
        f"DNS Lookup  : {check_dns()}",
        "==========================================",
    ]

    report = "\n".join(report_lines)
    print(report)

    filename = "diagnostic_report.txt"
    with open(filename, "w") as file:
        file.write(report)
    print(f"\nReport saved successfully to {os.path.abspath(filename)}")


if __name__ == "__main__":
    generate_report()
