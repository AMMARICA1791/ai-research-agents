SOURCE_EXCERPT = 'Available now: NVIDIA Nemotron 3.5 Bolt E4B 4GB ⚡️ Our newest small open model is built for local assistants, interactive characters and robots that can carry on a conversation and use tools to get things done. Watch Reachy Mini chat and move, with Bolt handling conversation and NVIDIA Cosmos handling vision. Both models run locally on Jetson Orin Nano 8GB. Learn more: https://research.nvidia.com/labs/nemotron/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB/ Me'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
