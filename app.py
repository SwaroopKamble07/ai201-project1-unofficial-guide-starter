import gradio as gr

from query import ask


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = result["sources"]
    if sources:
        sources_text = "\n".join(f"• {s}" for s in sources)
    else:
        sources_text = "(no sources — the guide didn't have enough information)"
    return result["answer"], sources_text


EXAMPLES = [
    "Are Canyon Creek Heights apartments furnished?",
    "Are the UTD dorms single occupancy or shared rooms?",
    "Do the Canyon Creek Heights apartments include utilities in rent?",
    "Is Canyon Creek Heights safe?",
    "Are there any problems with maintenance or insects?",
]

with gr.Blocks(title="The Unofficial Guide — UTD Housing") as demo:
    gr.Markdown(
        """
        # 🏠 The Unofficial Guide — UTD On-Campus Housing

        Ask about real student experiences with University of Texas at Dallas
        on-campus housing — dorms, University Village, Canyon Creek Heights, costs,
        safety, and more. Answers come **only** from collected student reviews and
        tour transcripts; if the guide doesn't know, it will say so.

        **How to use:** type a question below (or click an example), then press
        **Ask** or hit Enter.
        """
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Are Canyon Creek Heights apartments furnished?",
        lines=2,
    )
    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    gr.Examples(examples=EXAMPLES, inputs=inp)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
