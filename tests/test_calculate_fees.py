import pytest
from datetime import datetime, timedelta
from library_service import (
    calculate_late_fee_for_book
)
from database import (
    insert_borrow_record
)

def test_calculate_fees_book_not_overdue():
    """Calculate fees for book not overdue"""

    result = calculate_late_fee_for_book("123456", 3)
    
    assert result['fee_amount'] == 0
    assert result['days_overdue'] == 0

def test_calculate_fees_book_1_day_overdue():
    """Calculate fees for book 1 day overdue."""
    insert_borrow_record("444444", 4, datetime.now() + timedelta(days=15), datetime.now() - timedelta(days=1))
    result = calculate_late_fee_for_book("444444", 4)
    
    assert result['fee_amount'] == 0.5
    assert result['days_overdue'] == 1

def test_calculate_fees_book_overdue_nine(): 
    """Calculate fees for book 9 days overdue."""
    insert_borrow_record("555555", 4, datetime.now() - timedelta(days=23), datetime.now() - timedelta(days = 9))
    result = calculate_late_fee_for_book("555555", 4)
    
    assert result['fee_amount'] == 5.5
    assert result['days_overdue'] == 9

def test_calculate_fees_book_overdue_forty_one(): 
    """Calculate fees for a book 41 days overdue."""
    insert_borrow_record("666666", 4, datetime.now() - timedelta(days=55), datetime.now() - timedelta(days = 41))
    result = calculate_late_fee_for_book("666666", 4)
    
    assert result['fee_amount'] == 15
    assert result['days_overdue'] == 41

def test_calculate_fees_book_not_exist(): 
    """Calculate for a book that doesn't exist."""

    result = calculate_late_fee_for_book("123456", 99)
    
    assert result['status'] == "Invalid book"

def test_calculate_fees_book_not_borrowed(): 
    """Calculate for a patron that has not borrowed any books."""

    result = calculate_late_fee_for_book("999999", 1)
    
    assert result['status'] == "Invalid book"

