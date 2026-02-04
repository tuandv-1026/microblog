"""Unit tests for Markdown service."""

import pytest
from src.service.markdown_service import markdown_service


def test_render_basic_markdown():
    """Test basic Markdown rendering."""
    markdown = "# Hello World\n\nThis is a **test**."
    html = markdown_service.render(markdown)
    
    assert "<h1>Hello World</h1>" in html
    assert "<strong>test</strong>" in html


def test_render_code_block():
    """Test code block rendering."""
    markdown = """```python
def hello():
    print("Hello")
```"""
    html = markdown_service.render(markdown)
    
    assert "<code>" in html
    assert "def hello():" in html


def test_xss_prevention():
    """Test XSS attack prevention."""
    markdown = "Hello <script>alert('XSS')</script>"
    html = markdown_service.render(markdown)
    
    # Script tag should be stripped
    assert "<script>" not in html
    assert "alert" not in html


def test_generate_excerpt():
    """Test excerpt generation."""
    markdown = "# Title\n\n" + "This is a test. " * 50
    excerpt = markdown_service.generate_excerpt(markdown, max_length=100)
    
    assert len(excerpt) <= 110  # Some buffer for ellipsis
    assert excerpt.endswith("...")
    assert "Title" not in excerpt  # Headers should be stripped


def test_generate_excerpt_short_content():
    """Test excerpt generation with short content."""
    markdown = "Short content"
    excerpt = markdown_service.generate_excerpt(markdown, max_length=100)
    
    assert excerpt == "Short content"
    assert not excerpt.endswith("...")
