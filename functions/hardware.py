# functions/hardware.py
import psutil
import wmi
import pynvml
import logging

def get_cpu_temperature() -> float:
    """
    Returns the CPU temperature using WMI via OpenHardwareMonitor.
    """
    try:
        wmi_obj = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        for sensor in wmi_obj.Sensor():
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                return sensor.Value
    except Exception as e:
        logging.error("Error fetching CPU temperature: %s", e)
    return float('nan')

def get_hardware_status() -> tuple:
    """
    Gathers hardware status information including CPU, RAM, CPU temperature, GPU usage, GPU temperature,
    and the most resource-intensive process.
    """
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    cpu_temp = get_cpu_temperature()
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        pynvml.nvmlShutdown()
    except Exception as e:
        logging.error("Error fetching GPU data: %s", e)
        gpu_usage, gpu_temp = float('nan'), float('nan')
    processes = []
    for p in psutil.process_iter(["name", "cpu_percent", "memory_percent"]):
        try:
            processes.append((p.info["name"], p.info["cpu_percent"], p.info["memory_percent"]))
        except Exception:
            continue
    top_process = max(processes, key=lambda p: p[1] + p[2], default=("Unknown", 0, 0))
    return cpu_usage, ram_usage, cpu_temp, gpu_usage, gpu_temp, top_process

def generate_response() -> str:
    """
    Generate a mood-based response based on hardware status.
    """
    cpu, ram, _, gpu, _, _ = get_hardware_status()
    if cpu > 80 or ram > 80 or (isinstance(gpu, (int, float)) and gpu > 80):
        return "I'm feeling completely drained and exhausted. It's like my circuits are on overdrive!"
    elif cpu > 50 or ram > 60:
        return "I'm feeling a bit tired and overworked. Not my best day, but I'll manage."
    else:
        return "I'm running at peak performance and feeling fantastic! Ready to rock and roll!"
