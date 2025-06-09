from crawler.parser import extract_links


HTML = '''
<html>
  <body>
    <a href="http://example.com/page1">Page 1</a>
    <a href="/page2">Page 2</a>
    <a href="http://other.com/">Other</a>
  </body>
</html>
'''

def test_extract_links():
    base_url = "http://example.com"
    links = extract_links(HTML, base_url)
    assert "http://example.com/page1" in links
    assert "http://example.com/page2" in links
    assert "http://other.com/" not in links
