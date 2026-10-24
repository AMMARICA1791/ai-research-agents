SOURCE_EXCERPT = '🎯 OpenResearch now has @TrackioApp built in 📈 Your agent logs its experiments to Trackio, charts open right next to each run, and it reads the curves back to decide what to try next. Open source and local-first. Running on HF Jobs, Modal, k8s or Slurm? Save a @huggingface Space an…'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
