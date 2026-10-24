SOURCE_EXCERPT = 'Ahh… blue lagoon 🏖️ This deep-blue sea of gas and dust—called Messier 8 or the Lagoon Nebula—is a hotbed of star formation. The young stars within the nebula emit rays of high-energy light, including X-rays shown in pink by @chandraxray.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
