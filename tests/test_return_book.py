import pytest
from library_service import (
    return_book_by_patron,
    borrow_book_by_patron,
    add_book_to_catalog, 
    get_book_by_isbn
)

def test_return_book_valid_input(): 
    """Test borrowing a book with valid input."""
    add_book_to_catalog("Test Book 33", "Author 33", 3232323232324, 33)
    book = get_book_by_isbn(3232323232323)
    borrow_book_by_patron("939393", book['id'])
    success, message = return_book_by_patron("939393", book['id'])
    
    assert success == True
    assert "Book returned" in message

def test_return_book_invalid_book_not_borrowed_by_patron():
    """Test returning a book borrowed by a different patron."""
    success, message = return_book_by_patron("654321", 3)
    
    assert success == False
    assert "Book not borrowed" in message

def test_return_book_invalid_no_patron(): 
    """Test returning a book without a patron ID."""
    success, message = return_book_by_patron(None, 4)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_return_book_invalid_patron_id_too_long(): 
    """Test returning a book from an invalid patron id."""
    success, message = return_book_by_patron("1234567890", 4)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_return_book_invalid_book_id(): 
    """Test returning a book with an invalid ID."""
    success, message = return_book_by_patron("123456", 99)
    
    assert success == False
    assert "Invalid book ID" in message
