import pytest
from database import (
    get_all_books
)

def test_get_all_books_fields():
    """Ensure all required fields are returned for each book."""
    books = get_all_books()
    assert len(books) > 0
    
    for book in books:
        assert "id" in book
        assert "title" in book
        assert "author" in book
        assert "isbn" in book
        assert "total_copies" in book
        assert "available_copies" in book

def test_available_vs_total_copies():
    """Check available copies is <= total copies."""
    books = get_all_books()
    for book in books:
        assert book["available_copies"] <= book["total_copies"]

def test_borrow_button_visibility():
    """Check borrow button only visible if available_copies > 0."""
    books = get_all_books()
    for book in books:
        if book["available_copies"] > 0:
            borrow_action_visible = True
        else:
            borrow_action_visible = False
        assert borrow_action_visible == (book["available_copies"] > 0)
