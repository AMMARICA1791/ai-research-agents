SOURCE_EXCERPT = 'LIVE: @NASAAdmin and agency leaders are sharing the latest updates on next year&apos;s Artemis III mission and our plans to return astronauts to the surface of the Moon by 2028. https://x.com/i/broadcasts/1RJZzBdZYQgJB'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
