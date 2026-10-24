SOURCE_EXCERPT = 'NASA just shared some major updates on the road ahead for Artemis 🚀 2027: Artemis III tests Orion and two lunar landers in low Earth orbit. 2028: Artemis IV returns Americans to the Moon. Catch up on today&apos;s announcements in this special edition NASA Minute! Media'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
