# 📍 scripts/watch_data.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from src.pipelines.training_pipeline import run_training_pipeline


class DataHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            print(f"📂 New dataset detected: {event.src_path}")
            run_training_pipeline()


if __name__ == "__main__":
    path = "data/raw"
    observer = Observer()
    observer.schedule(DataHandler(), path, recursive=False)
    observer.start()

    print("👀 Watching data/raw for new files...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()