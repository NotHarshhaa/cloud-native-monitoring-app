import psutil
import logging
from flask import Flask, render_template

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

def get_metrics():
    """Fetch system metrics (CPU, memory, and temperature if available)."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Try to get CPU temperature (not available on all systems)
    try:
        temp_info = psutil.sensors_temperatures()
        cpu_temp = temp_info["coretemp"][0].current if "coretemp" in temp_info else None
    except AttributeError:
        cpu_temp = None  # Not supported on all OS

    return round(cpu_usage, 2), round(memory_usage, 2), cpu_temp

@app.route("/")
def index():
    """Renders the monitoring dashboard."""
    cpu_usage, memory_usage, cpu_temp = get_metrics()
    
    message = None
    if cpu_usage > 80 or memory_usage > 80:
        message = "⚠️ High CPU or Memory Usage! Consider scaling up."
    if cpu_temp and cpu_temp > 75:
        message = "🔥 CPU Temperature is too high! Consider cooling measures."

    logging.info(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Temp: {cpu_temp if cpu_temp else 'N/A'}")

    return render_template(
        "index.html",
        cpu_metric=cpu_usage,
        mem_metric=memory_usage,
        cpu_temp=cpu_temp if cpu_temp else "N/A",
        message=message
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
