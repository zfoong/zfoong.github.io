from pathlib import Path
from bs4 import BeautifulSoup
import pytest

HTML_FILES = list(Path('.').rglob('*.html'))

@pytest.mark.parametrize('html_file', HTML_FILES)
def test_links_exist(html_file):
    with open(html_file, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    for tag in soup.find_all(['link', 'script', 'img']):
        attr = 'href' if tag.name != 'img' else 'src'
        if not tag.has_attr(attr):
            continue
        target = tag[attr]
        if target.startswith(('http://', 'https://', '//', 'mailto:', '#')):
            continue
        path = (html_file.parent / target).resolve()
        assert path.exists(), f"Missing {target} referenced in {html_file}"
