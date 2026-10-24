SOURCE_EXCERPT = 'Article URL: https://www.apollo.com/wealth/insights-news/insights/daily-spark/no-signs-of-ai-payoff-outside-the-tech-sector Comments URL: https://news.ycombinator.com/item?id=50224463 Points: 156 # Comments: 110'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
