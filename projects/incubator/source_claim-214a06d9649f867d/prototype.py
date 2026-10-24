SOURCE_EXCERPT = 'NVIDIA CEO Jensen Huang asked 4 tiny robots to sit, stand, nap, and do somersaults. And they actually did it. NVIDIA is bringing AI agents from virtual world to real world with these robotic ducks. Media'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
