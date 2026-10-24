SOURCE_EXCERPT = 'Ready for an Artemis update? Tune in Friday, Oct. 23, at 2 p.m. ET (1800 UTC) to hear our latest progress and accelerated plans for Artemis lunar missions. Watch live: https://www.youtube.com/live/pAKqJxuxDgk'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
