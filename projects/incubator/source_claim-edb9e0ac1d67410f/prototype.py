SOURCE_EXCERPT = 'I wanted a read-aloud extension that could read from the Kindle Online Reader. The ones I tried used voices I did not enjoy listening to or had a UX that was too cluttered or annoying or needed a signup. So I decided to vibe code my own. It is open source and uses open weight models that run in the browser. https://swrdfish.github.io/Narro/ Comments URL: https://news.ycombinator.com/item?id=50224373 Points: 5 # Comments: 1'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
