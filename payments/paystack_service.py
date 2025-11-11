import requests
from django.conf import settings
import uuid


class PaystackService:
    """Service for handling Paystack payment operations"""
    
    BASE_URL = "https://api.paystack.co"
    
    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
    
    def initialize_payment(self, email, amount, order_id):
        """
        Initialize a payment transaction
        
        Args:
            email: Customer's email
            amount: Amount in kobo (multiply naira by 100)
            order_id: Order reference ID
        
        Returns:
            dict: Response from Paystack API
        """
        url = f"{self.BASE_URL}/transaction/initialize"
        
        # Generate unique reference
        reference = f"ORD-{order_id}-{uuid.uuid4().hex[:8].upper()}"
        
        payload = {
            "email": email,
            "amount": int(amount * 100),  # Convert to kobo
            "reference": reference,
            "callback_url": f"{settings.FRONTEND_URL}/payment/callback",
            "metadata": {
                "order_id": str(order_id)
            }
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def verify_payment(self, reference):
        """
        Verify a payment transaction
        
        Args:
            reference: Payment reference
        
        Returns:
            dict: Response from Paystack API
        """
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_payment_status(self, reference):
        """
        Get payment status
        
        Args:
            reference: Payment reference
        
        Returns:
            str: Payment status (success, failed, pending)
        """
        result = self.verify_payment(reference)
        
        if result.get('status') and result.get('data'):
            return result['data'].get('status', 'pending')
        
        return 'failed'
