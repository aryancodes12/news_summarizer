from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_tokens=100):
    if not text or len(text.split()) < 20:
        return text
    try:
        summary = summarizer(text, max_length=max_tokens, min_length=30, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        print("Error summarizing:", e)
        return text