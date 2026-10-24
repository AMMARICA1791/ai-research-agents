SOURCE_EXCERPT = 'Thank you @SPARC_NA for interviewing arXiv for #OAWeek! arXiv&apos;s CEO chatted with SPARC about the cost of knowledge &amp; what it takes to operate an essential open infrastructure in today&apos;s rapidly changing research landscape. Read the full profile here: https://www.openaccessweek.org/theme-profiles/arxiv'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
