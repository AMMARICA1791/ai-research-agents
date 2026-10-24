SOURCE_EXCERPT = 'NASA’s Inspiration Tour has landed in in the SEC 🚀🏈 Ahead of Alabama vs. Texas A&amp;M, @NASAAdmin met with students and fans outside Bryant-Denny Stadium, joined @SecRollins to sign a new MOU between NASA and @USDA , and will soon take to the skies for today’s flyover!'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
