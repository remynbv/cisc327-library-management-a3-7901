import pytest
from datetime import datetime, timedelta
from library_service import (
    get_patron_status_report, 
    borrow_book_by_patron
)
from database import (
    insert_borrow_record
)

def test_patron_status_valid_input(): 
    """Search a valid patron's information"""
    borrow_book_by_patron("657585", 4)
    result = get_patron_status_report("657585")

    assert result['patron_id'] == "657585"

def test_patron_status_valid_input_two(): 
    """Search a valid patron's information"""
    insert_borrow_record("444444", 4, datetime.now() - timedelta(days=16), datetime.now() - timedelta(days=2))
    result = get_patron_status_report("444444")
    """
    check = False
    for i in result['currently_borrowed']:
        if i['book_id']==4:
            check==True

    assert check == True
    """
    assert result['patron_id'] == "444444"
    assert result["total_late_fees"]>=0

def test_patron_status_nonexistent_patron(): 
    """Search a nonexistent patron's information"""

    result = get_patron_status_report("991100")
    
    assert result['status'] == "No information available" 

def test_patron_status_invalid_id_too_short(): 
    """Search a too short id"""

    result = get_patron_status_report("123")
    
    assert result['status'] == "Invalid patron ID" 

def test_patron_status_invalid_id_too_long(): 
    """Search a too long id"""

    result = get_patron_status_report("1234567890")
    
    assert result['status'] == "Invalid patron ID" 
