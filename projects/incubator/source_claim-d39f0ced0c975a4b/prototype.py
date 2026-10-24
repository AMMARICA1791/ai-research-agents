SOURCE_EXCERPT = 'Even the most regulated industries are going open-source 🤗 The AI question in financial services has moved from which model to use to where that model is allowed to run. New post with @TangriKunal and @huggingface on why firms want to run models on their own infrastructure, and how governance gets them approved to run there. Read it here…'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
