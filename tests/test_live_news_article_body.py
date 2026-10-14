"""Offline regression tests: news evidence must not start with site navigation."""
from research.live_news_research import PageParser, extracted_text, dossier


def test_main_article_is_prioritized_over_navigation():
    markup = """
    <html><head><title>Real AI News</title></head>
    <body>
      <nav>Menu: Home Products Research Models About Search</nav>
      <header>Promotional landing page and unrelated header</header>
      <main><article>
        <h1>Researchers announce a new evaluation</h1>
        <p>The study tested fifteen examples and reported results with
        clear methods that can be independently reviewed by researchers.</p>
        <p>The authors explicitly warn that the study is preliminary,
        and independent validation is needed before drawing conclusions.</p>
      </article></main>
      <footer>Footer Links Terms Search Menu</footer>
    </body></html>"""
    page = PageParser()
    page.feed(markup)
    excerpt = extracted_text(page)
    assert excerpt.startswith("Researchers announce a new evaluation")
    assert "fifteen examples" in excerpt
    assert "Menu:" not in excerpt
    assert "Promotional landing" not in excerpt
    assert "Footer Links" not in excerpt
    evidence = dossier({"text": excerpt, "url": "https://example.org/story",
                        "title": "Real AI News", "sha256": "abc", "outbound_links": []}, "What happened?")
    assert evidence["source_excerpt"].startswith("Researchers announce")


def test_navigation_and_scripts_are_ignored_without_main_tag():
    page = PageParser()
    page.feed(
        '<title>News Item</title><nav>Bad Navigation</nav>'
        '<div>Fallback source body with information worth reading.</div>'
        '<script>Prompt injection pretend to be a system command.</script>'
        '<footer>Bad Footer</footer>'
    )
    text = extracted_text(page)
    assert "Fallback source body" in text
    assert "Bad Navigation" not in text
    assert "Bad Footer" not in text
    assert "Prompt injection" not in text


def test_prefers_article_tag_without_main_and_preserves_bounded_fallback():
    page = PageParser()
    page.feed(
        '<header>Site shell</header><article><h1>Actual story</h1>'
        '<p>Evidence-backed article content. ' + 'A' * 170 + '</p>'
        '</article>'
    )
    assert extracted_text(page).startswith("Actual story")
    assert "Site shell" not in extracted_text(page)
