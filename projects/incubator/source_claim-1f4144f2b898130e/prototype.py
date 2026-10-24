SOURCE_EXCERPT = 'SynthID timeline over the last few weeks has been momentous – from opening SynthID Detector to the public, to launching SynthID Bio to watermark functional, AI-designed proteins. Each moment brought us a step closer to our broader vision on provenance, or helping verify what is AI-generated and what isn’t. Recently, Dartmouth Professor Hany Farid and I discussed why solving provenance is vital to @GoogleDeepMind’s broader mission to develop AI to'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
