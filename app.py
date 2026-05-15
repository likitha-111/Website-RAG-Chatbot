import threading
import uvicorn

from api.main import app


def run_api():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )

if __name__ == "__main__":

    api_thread = threading.Thread(
        target=run_api
    )

    api_thread.start()

    from ui.gradio_ui import demo

    demo.launch()