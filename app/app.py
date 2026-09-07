import os

import psycopg
from flask import Flask

app = Flask(__name__)


def get_database_connection():
    database_url = os.environ["DATABASE_URL"]
    return psycopg.connect(database_url)


def get_latest_metrics():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    collected_at,
                    hostname,
                    cpu_count,
                    cpu_percent,
                    memory_percent,
                    disk_percent,
                    os_info
                FROM system_metrics
                ORDER BY collected_at DESC
                LIMIT 1
                """
            )

            return cursor.fetchone()


@app.route("/")
def home():
    metrics = get_latest_metrics()

    if metrics is None:
        return """
        <html>
            <head>
                <title>SRE Kubernetes Monitor</title>
            </head>
            <body>
                <h1>SRE Kubernetes Monitor</h1>
                <p>No system metrics have been collected yet.</p>
            </body>
        </html>
        """

    (
        collected_at,
        hostname,
        cpu_count,
        cpu_percent,
        memory_percent,
        disk_percent,
        os_info,
    ) = metrics

    return f"""
    <html>
        <head>
            <title>SRE Kubernetes Monitor</title>
        </head>
        <body>
            <h1>SRE Kubernetes Monitor</h1>

            <h2>Latest System Metrics</h2>

            <p><strong>Hostname:</strong> {hostname}</p>
            <p><strong>CPU count:</strong> {cpu_count}</p>
            <p><strong>CPU utilisation:</strong> {cpu_percent}%</p>
            <p><strong>Memory utilisation:</strong> {memory_percent}%</p>
            <p><strong>Disk utilisation:</strong> {disk_percent}%</p>
            <p><strong>Operating system:</strong> {os_info}</p>
            <p><strong>Last collection:</strong> {collected_at}</p>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/ready")
def ready():
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

        return {"status": "ready"}, 200

    except Exception:
        return {"status": "not ready"}, 503
