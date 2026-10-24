SOURCE_EXCERPT = 'Using a single Nano Banana image and Blender MCP, Gemini 4 Argon built a 3D Gothic cathedral in @Antigravity. It iterates on the geometry, textures, and lighting to create the finished scene. Media'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
