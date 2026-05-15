import gradio as gr

from rag.chatbot import ask_chatbot, memory


def chat_fn(message, history):

    if not history:
        memory.clear()

    response = ask_chatbot(message)

    answer = response["answer"]

    unique_sources = []
    seen_urls = set()
    for s in response.get("sources", []):
        if s["url"] not in seen_urls:
            unique_sources.append(s)
            seen_urls.add(s["url"])

    if unique_sources:
        sources_text = "\n\n".join(
            [f"{s['title']}\n{s['url']}" for s in unique_sources]
        )
        final_response = f"{answer}\n\nSources:\n{sources_text}"
    else:
        final_response = answer

    return final_response


with gr.Blocks() as demo:

    gr.Markdown("# TechCrunch Website RAG Chatbot")

    chatbot = gr.ChatInterface(
        fn=chat_fn
    )

demo.launch()