try:
    import pytest
except ImportError:
    pytest = None
from app.scraper.parser import clean_html, generate_content_hash, categorize_article, parse_rss_feed

SAMPLE_RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>TTD News</title>
    <link>https://news.tirumala.org</link>
    <item>
      <title><![CDATA[TTD to release online quota for ₹300 Special Entry Darshan for the month of May]]></title>
      <link>https://news.tirumala.org/press-release-may-sed-quota</link>
      <pubDate>Thu, 24 Apr 2026 10:00:00 +0000</pubDate>
      <description><![CDATA[<p>Tirumala Tirupati Devasthanams (TTD) will release the online quota for SED on ttdevasthanams.ap.gov.in.</p>]]></description>
    </item>
  </channel>
</rss>
"""

def test_clean_html():
    raw = "<p>Welcome to <b>Tirumala</b> &amp; holy hills!&nbsp;</p>"
    clean = clean_html(raw)
    assert clean == "Welcome to Tirumala & holy hills!"

def test_generate_content_hash():
    url = "https://news.tirumala.org/sample-1"
    title = "TTD Quota Release"
    h1 = generate_content_hash(url, title)
    h2 = generate_content_hash(url, title)
    assert h1 == h2
    assert len(h1) == 64

def test_categorize_article():
    darshan_cat = categorize_article("₹300 Special Entry Darshan online booking", "Quota release for pilgrims")
    assert darshan_cat["slug"] == "darshan"
    assert darshan_cat["is_quota"] is True

    seva_cat = categorize_article("Srivari Seva voluntary registration notice", "Devotees aged 18 to 60")
    assert seva_cat["slug"] == "srivari-seva"

    room_cat = categorize_article("Tirumala Cottage room quota notice", "Accommodation caution deposit")
    assert room_cat["slug"] == "accommodation"

def test_parse_rss_feed():
    articles = parse_rss_feed(SAMPLE_RSS_XML)
    assert len(articles) == 1
    art = articles[0]
    assert "₹300 Special Entry Darshan" in art["title_en"]
    assert art["source_domain"] == "news.tirumala.org"
    assert art["category_slug"] == "darshan"
    assert art["is_quota_alert"] is True
