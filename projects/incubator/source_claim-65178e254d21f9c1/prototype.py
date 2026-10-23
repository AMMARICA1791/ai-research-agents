SOURCE_EXCERPT = 'arXiv:2610.15884v3 Announce Type: replace-cross Abstract: False retry permission (FRP) occurs when an agent retries a timed-out tool call without support from the visible contract. RetryBench separates this error from realized recovery. Successful protected recovery does not imply reliable rejection of unsupported retries. In a 720-response key control, valid keys usually enabled safe progress, but offered changed keys elicited unsupported retrie'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
