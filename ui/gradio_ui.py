import uuid

import gradio as gr
import requests

from rag.chatbot import ask_chatbot


def create_new_session():
    return str(uuid.uuid4())


def initialize_session():
    return create_new_session()


def reset_session():
    return create_new_session()


def chat_fn(message, history, session_id):

    response = ask_chatbot(
        query=message,
        session_id=session_id
    )

    answer = response["answer"]

    unique_sources = []
    seen_urls = set()

    for s in response.get("sources", []):

        if s["url"] not in seen_urls:

            unique_sources.append(s)

            seen_urls.add(s["url"])

    if unique_sources:

        sources_text = "\n\n".join(
            [
                f"{s['title']}\n{s['url']}"
                for s in unique_sources
            ]
        )

        final_response = (
            f"{answer}\n\nSources:\n{sources_text}"
        )

    else:
        final_response = answer

    return final_response


def trigger_build():

    try:

        response = requests.post(
            "http://127.0.0.1:8000/build"
        )

        if response.status_code == 200:

            return response.json().get(
                "status",
                "Vector DB updated successfully!"
            )

        return f"Error: {response.status_code}"

    except Exception as e:

        return f"Error: {str(e)}"


with gr.Blocks() as demo:

    session_id = gr.State()

    demo.load(
        fn=initialize_session,
        inputs=None,
        outputs=session_id
    )

    gr.Markdown(
        "# TechCrunch Website RAG Chatbot"
    )

    with gr.Row():

        with gr.Column(scale=1):

            update_db_btn = gr.Button(
                "Update Vector DB"
            )

            update_status = gr.Textbox(
                label="Status",
                interactive=False
            )

            update_db_btn.click(
                fn=trigger_build,
                inputs=None,
                outputs=update_status
            )

        with gr.Column(scale=4):

            chatbot = gr.ChatInterface(
                fn=chat_fn,
                additional_inputs=[session_id]
            )
            chatbot.chatbot.clear(
                fn=reset_session,
                inputs=None,
                outputs=session_id
            )


if __name__ == "__main__":

    demo.launch()