# Project Implementation Status
Rémy Brown-Vandervecht, 20397901, Section 001, Group 1

| Function Name | Implementation Status | What is Missing |
| --------------| ----------------------| ----------------|
| add_book_to_catalog | Complete | N.A. |
| Catalog Display | Complete | N.A. |
| borrow_book_by_patron | Complete | N.A. |
| return_book_by_patron | Not Implemented | Verifies book was borrowed, updates available copies, record return date, calculate and display late fees |
| calculate_late_fee_for_book | Not Implemented | Calculate late fees, return JSON with fee amount and days overdue |
| search_books_in_catalog | Not Implemented | Allow partial matching for title/author, allow exact matching for ISBM, return catalog display results |
| get_patron_status_report | Not Implemented | Display borrowed books and their due dates, total late fees, number of books currently borrowed, and borrowing history |

| Test Script   | Checks | To be Expanded* |
| -------------------| ----------| ---------------|
| addBookTests       | Valid inputs, checks for existing copies | - |
| borrowBookTests    | Valid inputs, borrow unavailable/nonexistent books, max borrow limit | - |
| returnBookTests    | Valid inputs, book borrowed by patron | Confirm updated number of copies, record return dates |
| calculateFeesTests | Valid inputs, verifies fees applied properly | - |
| searchBooksTests   | Valid inputs, book/author/ISBM exists, no search input | - |
| patronStatusTests  | Valid input, patron exists | Confirm accurate displayed information |

*I felt these tests could not be properly implemented without having a better idea of how their respective functions would work. 