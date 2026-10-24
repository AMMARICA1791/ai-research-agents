SOURCE_EXCERPT = 'Over half of reported crimes in Singapore use sophisticated social engineering. With @GovTechSG, we’re building on-device fraud detection using our open model Gemma. By fine-tuning it on local scam tactics, it identifies threats in real time without compromising personal privacy → https://goo.gle/4ygVkJa'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
