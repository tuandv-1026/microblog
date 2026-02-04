"""Markdown rendering service with XSS protection."""

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.nl2br import Nl2BrExtension
import bleach
from typing import List

# Allowed HTML tags after markdown rendering
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'hr', 'div', 'span',
    'ul', 'ol', 'li', 'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
]

# Allowed HTML attributes
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],
}

# Allowed URL protocols
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


class MarkdownService:
    """Service for rendering Markdown to HTML with XSS protection."""
    
    def __init__(self):
        """Initialize Markdown processor with extensions."""
        self.md = markdown.Markdown(
            extensions=[
                'extra',
                'nl2br',
                'sane_lists',
                FencedCodeExtension(),
                CodeHiliteExtension(css_class='highlight'),
                TableExtension(),
            ],
            output_format='html5',
        )
    
    def render(self, markdown_text: str) -> str:
        """
        Render Markdown to sanitized HTML.
        
        Args:
            markdown_text: Raw Markdown text
            
        Returns:
            Sanitized HTML string
        """
        # Convert Markdown to HTML
        html = self.md.convert(markdown_text)
        
        # Sanitize HTML to prevent XSS
        clean_html = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
        )
        
        # Reset Markdown processor for next use
        self.md.reset()
        
        return clean_html
    
    def generate_excerpt(self, markdown_text: str, max_length: int = 200) -> str:
        """
        Generate a plain text excerpt from Markdown.
        
        Args:
            markdown_text: Raw Markdown text
            max_length: Maximum length of excerpt
            
        Returns:
            Plain text excerpt
        """
        # Convert to HTML first
        html = self.md.convert(markdown_text)
        
        # Strip all HTML tags
        plain_text = bleach.clean(html, tags=[], strip=True)
        
        # Truncate and add ellipsis if needed
        if len(plain_text) > max_length:
            plain_text = plain_text[:max_length].rsplit(' ', 1)[0] + '...'
        
        # Reset Markdown processor
        self.md.reset()
        
        return plain_text.strip()


# Singleton instance
markdown_service = MarkdownService()
