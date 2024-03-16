import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".html") and "templates" in event.src_path:
            # Replace 'app.py' with the actual command to run your app
            os.system("python app.py")


if __name__ == "__main__":
    os.system("python app.py")
    print("Watching for changes in 'templates' directory")
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
