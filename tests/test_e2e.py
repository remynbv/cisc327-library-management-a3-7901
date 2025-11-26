from flask import url_for
from playwright.sync_api import Page, expect

def test_e2e_one(page:Page): 
    """Test: Add new book, verify it appears, go to book borrow, borrow w/ patron ID, verify confirmation message"""
    """Use playwright codegen http://127.0.0.1:5000/ to run codegen"""
    """pytest tests/test_e2e.py to run tests"""

    page.goto("http://localhost:5000/")
    page.get_by_role("link", name="➕ Add Book").click()
    page.get_by_role("textbox", name="Title").click()
    page.get_by_role("textbox", name="Title").fill("The Count of Monte Cristo")
    page.get_by_role("textbox", name="Author").click()
    page.get_by_role("textbox", name="Author").fill("Alexandre Dumas")
    page.get_by_role("textbox", name="ISBN").click()
    page.get_by_role("textbox", name="ISBN").fill("4217329972123")
    page.get_by_role("spinbutton", name="Total Copies").click()
    page.get_by_role("spinbutton", name="Total Copies").fill("5")
    page.get_by_role("button", name="Add Book to Catalog").click()

    expect(page.get_by_text("successfully added")).to_be_visible()

    page.get_by_role("row").filter(has_text="The Count of Monte Cristo").get_by_placeholder("Patron ID (6 digits)").click()
    page.get_by_role("row").filter(has_text="The Count of Monte Cristo").get_by_placeholder("Patron ID (6 digits)").fill("421732")
    page.get_by_role("row", name="Count of Monte Cristo").get_by_role("button", name="Borrow").click()
    
    expect(page.get_by_text("Successfully borrowed")).to_be_visible()

def test_e2e_two(page:Page):
    """Search for an existing book, verify one's unavailable, attempt to return non-existent book, confirm error"""
    page.goto("http://localhost:5000/")
    page.get_by_role("link", name="🔍 Search").click()
    page.get_by_role("textbox", name="Search Term").click()
    page.get_by_role("textbox", name="Search Term").fill("mockingbird")
    page.get_by_role("button", name="🔍 Search").click()

    expect(page.get_by_text("Not Available")).to_be_visible()

    page.get_by_role("link", name="↩️ Return Book").click()
    page.get_by_role("textbox", name="Patron ID").click()
    page.get_by_role("textbox", name="Patron ID").fill("794232")
    page.get_by_role("spinbutton", name="Book ID").click()
    page.get_by_role("spinbutton", name="Book ID").fill("3")
    page.get_by_role("button", name="Process Return").click()
    
    expect(page.get_by_text("Book not borrowed")).to_be_visible()

def test_e2e_three(page:Page):
    """Borrow a book, return a book, verify return and no fees"""
    page.goto("http://localhost:5000/")

    page.get_by_role("row").filter(has_text="Dune").get_by_placeholder("Patron ID (6 digits)").click()
    page.get_by_role("row").filter(has_text="Dune").get_by_placeholder("Patron ID (6 digits)").fill("071930")
    page.get_by_role("row", name="Dune").get_by_role("button", name="Borrow").click()

    expect(page.get_by_text("Successfully borrowed")).to_be_visible()

    page.get_by_role("link", name="↩️ Return Book").click()

    page.get_by_role("textbox", name="Patron ID").click()
    page.get_by_role("textbox", name="Patron ID").fill("071930")
    page.get_by_role("spinbutton", name="Book ID").click()
    page.get_by_role("spinbutton", name="Book ID").fill("1")
    
    page.get_by_role("button", name="Process Return").click()

    expect(page.get_by_text("Book returned successfully")).to_be_visible()