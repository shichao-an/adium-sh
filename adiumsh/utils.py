import psutil


def is_process_running(process_name):
    names = [proc.name() for proc in psutil.process_iter()]
    return process_name in names
