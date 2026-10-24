SOURCE_EXCERPT = 'Article URL: https://noyb.eu/en/ai-eu-member-states-approve-digital-expropriation-europeans-ai-companies Comments URL: https://news.ycombinator.com/item?id=50223856 Points: 3 # Comments: 2'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
