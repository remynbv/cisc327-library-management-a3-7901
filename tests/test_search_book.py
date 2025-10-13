import pytest
from library_service import (
    search_books_in_catalog
)

def test_search_valid_title(): 
    """Search a book in the catalogue"""

    result = search_books_in_catalog("Great Gatsby", "Title")
    
    check = False
    for i in result:
        if "reat" in i['title']:
            check = True

    assert check == True

def test_search_valid_author(): #Fixed
    """Search an author in the catalogue"""

    result = search_books_in_catalog("Frank Herbert", "Author")
    
    check = False
    checkTwo = False
    for i in result:
        if "Dune" in i['title']:
            check = True

    assert check == True

def test_search_valid_id(): 
    """Search an ID in the catalogue"""

    result = search_books_in_catalog("9780061120084", "ISBN")
    
    assert len(result)==1

def test_search_invalid_id(): 
    """Search an invalid ID in the catalogue"""

    result = search_books_in_catalog("1001001001001000100101011", "ISBN")
    
    assert "No results found" in result

def test_search_no_search_input(): 
    """Search with no input"""

    result = search_books_in_catalog(None, "Title")
    
    assert any("Mockingbird" in b["title"] for b in result)
    assert any("Dune" in b["title"] for b in result)
    assert any("Scott" in b["author"] for b in result)
    assert any("Harper Lee" in b["author"] for b in result)
