SOURCE_EXCERPT = "Imagine this. You can control Alexa with your voice and ask it to play songs, remember grocery lists, add reminders to your calendar. Elon Musk's Neuralink can interface with your brain and reduce the latency with which you can communicate with computers. What if you had AI applied to your brain and you could train it to think like you just like how you train your agents at work? Comments URL: https://news.ycombinator.com/item?id=50223726 Points:"
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
