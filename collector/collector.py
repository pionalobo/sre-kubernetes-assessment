import os
import platform
import socket
from datetime import datetime, timezone

import psutil
import psycopg


def collect_system_metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "collected_at": datetime.now(timezone.utc),
        "hostname": socket.gethostname(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_total": memory.total,
        "memory_available": memory.available,
        "memory_percent": memory.percent,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": disk.percent,
        "os_info": platform.platform(),
    }


def save_metrics(metrics):
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO system_metrics (
                    collected_at,
                    hostname,
                    cpu_count,
                    cpu_percent,
                    memory_total,
                    memory_available,
                    memory_percent,
                    disk_total,
                    disk_used,
                    disk_percent,
                    os_info
                )
                VALUES (
                    %(collected_at)s,
                    %(hostname)s,
                    %(cpu_count)s,
                    %(cpu_percent)s,
                    %(memory_total)s,
                    %(memory_available)s,
                    %(memory_percent)s,
                    %(disk_total)s,
                    %(disk_used)s,
                    %(disk_percent)s,
                    %(os_info)s
                )
                """,
                metrics,
            )


if __name__ == "__main__":
    metrics = collect_system_metrics()
    save_metrics(metrics)

    print("System metrics collected and stored successfully.")
    print(f"Collected at: {metrics['collected_at']}")
    print(f"Hostname: {metrics['hostname']}")
    print(f"CPU: {metrics['cpu_percent']}%")
    print(f"Memory: {metrics['memory_percent']}%")
    print(f"Disk: {metrics['disk_percent']}%")