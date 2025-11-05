
def analyze_text(text):
    # very simple summarizer placeholder: return first 200 chars and split words as keywords
    text = str(text)
    summary = text[:400] + ("..." if len(text) > 400 else "")
    words = [w.strip(".,؛:()\"'") for w in text.split() if len(w)>4]
    keywords = sorted(set(words), key=lambda s: -len(s))[:10]
    return {"summary": summary, "keywords": keywords}
