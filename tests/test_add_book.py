import pytest
from library_service import (
    add_book_to_catalog
)

def test_add_book_valid_input(): 
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book 2", "Test Author 2", "1234567890124", 6)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with ISBN too long."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "12345678901234567890123", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_no_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog(None, "Test Author", "1234567890123", 5)
    
    assert success == False
    assert "Title is required" in message

def test_add_book_invalid_title_too_long():
    """Test adding a book with title too long."""
    success, message = add_book_to_catalog("Test Book 1 Test Book 2 Test Book 3 Test Book 4 Test Book 5 Test Book 6 Test Book 7 Test Book 8 Test Book 9 Test Book 10 Test Book 11 Test Book 12 Test Book 13 Test Book 14 Test Book 15 Test Book 16 Test Book 17 Test Book 18 Test Book 19 Test Book 20 Test Book 21 Test Book 22 Test Book 23 Test Book 24 Test Book 25", "Test Author", "1234567890123", 5)
    
    assert success == False
    assert "200 characters" in message

def test_add_book_invalid_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Test Book", None, "1234567890123", 5)
    
    assert success == False
    assert "Author is required" in message

def test_add_book_invalid_total_copies_not_integer():
    """Test adding a book with non-integer total copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", "Nope")
    
    assert success == False
    assert "positive integer" in message

def test_add_book_invalid_negative_copies():
    """Test adding a book with negative copiest."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", -5)
    
    assert success == False
    assert "positive integer" in message

def test_add_book_invalid_zero_copies():
    """Test adding a book with negative copiest."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 0)
    
    assert success == False
    assert "positive integer" in message

def test_add_book_invalid_author_too_long(): 
    """Test adding a book with too long author name."""
    success, message = add_book_to_catalog("Test Book", "Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author Test Author ", "1234567890123", 5)
    
    assert success == False
    assert "less than 100" in message

def test_add_book_invalid_duplicate_input(): 
    """Test adding a duplicate book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    successTwo, messageTwo = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert successTwo == False
    assert "ISBN already exists" in messageTwo
