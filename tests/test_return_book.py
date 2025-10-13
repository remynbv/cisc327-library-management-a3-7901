import pytest
from library_service import (
    return_book_by_patron,
    borrow_book_by_patron,
    add_book_to_catalog
)

def test_return_book_valid_input(): # Failed: TODO: Fixed
    """Test borrowing a book with valid input."""
    add_book_to_catalog("Test Book 32", "Author 32", 3232323232323, 32)
    borrow_book_by_patron("939393", 32)
    success, message = return_book_by_patron("939393", 32)
    
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
