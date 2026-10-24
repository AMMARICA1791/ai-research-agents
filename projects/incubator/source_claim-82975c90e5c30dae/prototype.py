SOURCE_EXCERPT = 'That&apos;s our jam 🎼 Astronomers used @ChandraXray to find out that this radio wave formation, known as the &quot;Treble Clef&quot; thanks to its distinctive shape, was likely caused by an outburst from a supermassive black hole, followed by a collision of two galaxy clusters.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
