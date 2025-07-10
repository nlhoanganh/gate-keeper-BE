import threading

def execute_job(job, parameters: tuple=()):
    worker = threading.Thread(target=job, args=parameters)
    worker.start()