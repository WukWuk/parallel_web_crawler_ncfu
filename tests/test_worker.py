import pytest
from unittest.mock import patch, Mock
from crawler.worker import crawl_page

HTML_SAMPLE = '''
<html>
  <body>
    <a href="http://example.com/page1">Link1</a>
    <a href="/page2">Link2</a>
  </body>
</html>
'''

@patch("requests.get")
def test_crawl_page_success(mock_get):
    # Мокируем успешный ответ
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = HTML_SAMPLE
    mock_get.return_value = mock_response

    url = "http://example.com"
    depth = 0

    links = crawl_page(url, depth)
    assert "http://example.com/page1" in links
    assert "http://example.com/page2" in links

@patch("requests.get")
def test_crawl_page_http_error(mock_get):
    # Мокируем ошибочный статус
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = ""
    mock_get.return_value = mock_response

    links = crawl_page("http://example.com", 0)
    assert links == set()

@patch("requests.get")
def test_crawl_page_request_exception(mock_get):
    # Мокируем исключение при запросе
    mock_get.side_effect = Exception("Network error")
    links = crawl_page("http://example.com", 0)
    assert links == set()
