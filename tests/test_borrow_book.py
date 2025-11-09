import pytest
from datetime import datetime, timedelta
from services.library_service import (
    borrow_book_by_patron,
    add_book_to_catalog, 
    get_book_by_isbn
)
from database import (
    insert_borrow_record
)

def test_borrow_book_valid_input(): 
    """Test borrowing a book with valid input."""
    add_book_to_catalog("Test Book 32", "Author 32", 3131313131315, 32)
    book = get_book_by_isbn(3131313131315)
    success, message = borrow_book_by_patron("232323", book['id'])
    
    assert success == True
    assert "Successfully borrowed" in message

def test_borrow_book_invalid_no_patron_id():
    """Test borrowing a book with no patron id."""
    success, message = borrow_book_by_patron(None, 4)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_borrow_book_invalid_patron_id_too_long():
    """Test borrowing a book with patron id too long."""
    success, message = borrow_book_by_patron("1234567890", 3)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_borrow_book_invalid_patron_id_too_short():
    """Test borrowing a book with patron id too short."""
    success, message = borrow_book_by_patron("12", 4)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_borrow_book_invalid_book_nonexistent(): 
    """Test borrowing a book when book doesn't exist."""
    success, message = borrow_book_by_patron("123456", 99)
    
    assert success == False
    assert "Book not found" in message

def test_borrow_book_invalid_book_unavailable():
    """Test borrowing a book with book is unavailable."""
    success, message = borrow_book_by_patron("000000", 3) #Make it unavailable
    success, message = borrow_book_by_patron("123456", 3) 
    
    assert success == False
    assert "currently not available" in message

def test_borrow_book_invalid_too_many_books(): # Fixed
    """Test borrowing a book when patron has borrowed >5 books."""
    add_book_to_catalog("Test Book 11", "Test Author 11", "1101101101101", 11)
    add_book_to_catalog("Test Book 12", "Test Author 12", "1201201201201", 12)
    add_book_to_catalog("Test Book 13", "Test Author 13", "1301301301301", 13)
    add_book_to_catalog("Test Book 14", "Test Author 14", "1401401401401", 14)
    add_book_to_catalog("Test Book 15", "Test Author 15", "1501501501501", 15)
    add_book_to_catalog("Test Book 16", "Test Author 16", "1601601601601", 16)
    borrow_book_by_patron("456456", 11)
    borrow_book_by_patron("456456", 12)
    borrow_book_by_patron("456456", 13)
    borrow_book_by_patron("456456", 14)
    borrow_book_by_patron("456456", 15)
    success, message = borrow_book_by_patron("456456", 16) #Should have 5 already borrowed when attempting
    
    assert success == False

