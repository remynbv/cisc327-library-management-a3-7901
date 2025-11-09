import pytest
from unittest.mock import Mock, patch
from services.library_service import (
    pay_late_fees,
    refund_late_fee_payment
)
from services.payment_service import PaymentGateway

"""
pay_late_fees:
- Successful payment
- Payment declined by gateway
- Invalid patron ID (verify mock not called)
- Zero late fees (verify mock not called)
- Network error exception handling

refund_late_fee_payment:
- Successful refund 
- Invalid transaction ID rejection
- Invalid refund amount (negative, zero, more than 15$)

    
    Mocking example: 
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
        success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
"""

def test_pay_late_fee_success(): 
    """Test a successful transaction"""
    with patch("services.library_service.calculate_late_fee_for_book") as mockCalcFee:
        with patch("services.library_service.get_book_by_id") as mockGetBook:
            mockCalcFee.return_value = {'fee_amount': 5.5, 'days_overdue': 9, 'status':"Calculation complete"}
            mockGetBook.return_value = {'id': 4, 'title': 'Dune', 'available_copies': 3}
            mockGate = Mock(spec=PaymentGateway)
            mockGate.process_payment.return_value = (True, "txn_123", "Success")
            result, msg, txn = pay_late_fees("555555", 4, mockGate)

            assert result == True
            assert "successful" in msg
            mockGate.process_payment.assert_called_once_with(
                patron_id="555555", amount=5.5, description="Late fees for 'Dune'")

def test_pay_late_fee_gateway_decline(): 
    """Test payment declined by gateway"""
    with patch("services.library_service.calculate_late_fee_for_book") as mockCalcFee:
        with patch("services.library_service.get_book_by_id") as mockGetBook:
            mockCalcFee.return_value = {'fee_amount': 5.5, 'days_overdue': 9, 'status':"Calculation complete"}
            mockGetBook.return_value = {'id': 4, 'title': 'Dune', 'available_copies': 3}
            mockGate = Mock(spec=PaymentGateway)
            mockGate.process_payment.return_value = (False, "", "Failure")
            result, msg, txn = pay_late_fees("555555", 4, mockGate)

            assert result == False
            assert "Payment failed" in msg
            mockGate.process_payment.assert_called_once_with(
                patron_id="555555", amount=5.5, description="Late fees for 'Dune'")

def test_pay_late_fee_invalid_patron_id(): 
    """Test payment for an invalid patron ID"""
    with patch("services.library_service.calculate_late_fee_for_book") as mockCalcFee:
        with patch("services.library_service.get_book_by_id") as mockGetBook:
            mockCalcFee.return_value = {'status': 'Invalid book', 'fee_amount': 0.0, 'days_overdue': 0}
            mockGetBook.return_value = {'id': 4, 'title': 'Dune', 'available_copies': 3}
            mockGate = Mock(spec=PaymentGateway)
            mockGate.process_payment.return_value = (False, "", "Failure")
            result, msg, txn = pay_late_fees("1234567890", 4, mockGate)

            assert result == False
            assert "Invalid patron ID" in msg
            mockGate.process_payment.assert_not_called()

def test_pay_late_fee_no_late_fees(): 
    """Test payment when no fees are due"""
    with patch("services.library_service.calculate_late_fee_for_book") as mockCalcFee:
        with patch("services.library_service.get_book_by_id") as mockGetBook:
            mockCalcFee.return_value = {'fee_amount': 0, 'days_overdue': 0, 'status':"Calculation complete"}
            mockGetBook.return_value = {'id': 4, 'title': 'Dune', 'available_copies': 3}
            mockGate = Mock(spec=PaymentGateway)
            mockGate.process_payment.return_value = (True, "txn_123", "Success")
            result, msg, txn = pay_late_fees("555555", 4, mockGate)

            assert result == False
            assert "No late fees" in msg
            mockGate.process_payment.assert_not_called()

def test_pay_late_fee_network_error(): 
    """Test behaviour upon payment gateway error"""
    with patch("services.library_service.calculate_late_fee_for_book") as mockCalcFee:
        with patch("services.library_service.get_book_by_id") as mockGetBook:
            mockCalcFee.return_value = {'fee_amount': 5.5, 'days_overdue': 9, 'status':"Calculation complete"}
            mockGetBook.return_value = {'id': 4, 'title': 'Dune', 'available_copies': 3}
            mockGate = Mock(spec=PaymentGateway)
            mockGate.process_payment.side_effect = Exception("Network Error")
            result, msg, txn = pay_late_fees("555555", 4, mockGate)

            assert result == False
            assert "Payment processing error" in msg
            assert "Network Error" in msg
            mockGate.process_payment.assert_called_once_with(
                patron_id="555555", amount=5.5, description="Late fees for 'Dune'")

def test_refund_fee_success(): 
    """Test successful refund"""
    mockGate = Mock(spec=PaymentGateway)
    mockGate.refund_payment.return_value = (True, "processed successfully")
    result, msg = refund_late_fee_payment("txn_123", 5.5, mockGate)

    assert result == True
    assert "success" in msg
    mockGate.refund_payment.assert_called_once_with(
        "txn_123", 5.5)

def test_refund_fee_invalid_transaction_id(): 
    """Test refund with invalid ID"""
    mockGate = Mock(spec=PaymentGateway)
    mockGate.refund_payment.return_value = (True, "processed successfully")
    result, msg = refund_late_fee_payment("nah", 5.5, mockGate)

    assert result == False
    assert "Invalid transaction" in msg
    mockGate.refund_payment.assert_not_called()

def test_refund_fee_negative_amount(): 
    """Test refund for negative amount"""
    mockGate = Mock(spec=PaymentGateway)
    mockGate.refund_payment.return_value = (True, "processed successfully")
    result, msg = refund_late_fee_payment("txn_123", -9, mockGate)

    assert result == False
    assert "must be greater" in msg
    mockGate.refund_payment.assert_not_called()

def test_refund_fee_amount_too_large(): 
    """Test refund with invalidly large amount"""
    mockGate = Mock(spec=PaymentGateway)
    mockGate.refund_payment.return_value = (True, "processed successfully")
    result, msg = refund_late_fee_payment("txn_123", 42, mockGate)

    assert result == False
    assert "exceeds maximum late fee" in msg
    mockGate.refund_payment.assert_not_called()

def test_refund_fee_network_error(): 
    """What test does"""
    mockGate = Mock(spec=PaymentGateway)
    mockGate.refund_payment.side_effect = Exception("Network Error")
    result, msg = refund_late_fee_payment("txn_123", 5.5, mockGate)

    assert result == False
    assert "Refund processing error" in msg
    assert "Network Error" in msg
    mockGate.process_payment.assert_not_called()