from typing import Dict, Any, Optional
from datetime import datetime
import stripe
from sqlalchemy.orm import Session
from ..models.payment import Payment
from ..models.contribution import Contribution
from ..core.config import settings
from ..core.utils import format_currency

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_payment_intent(
        self,
        amount: float,
        currency: str = "usd",
        payment_method_types: list = ["card"],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a Stripe payment intent."""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                payment_method_types=payment_method_types,
                metadata=metadata
            )

            return {
                "status": "success",
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except stripe.error.StripeError as e:
            return {"status": "error", "message": str(e)}

    def process_payment(
        self,
        payment_intent_id: str,
        contribution_id: int
    ) -> Dict[str, Any]:
        """Process a payment and update contribution status."""
        try:
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status != "succeeded":
                return {"status": "error", "message": "Payment not successful"}

            # Get contribution
            contribution = self.db.query(Contribution).filter(
                Contribution.id == contribution_id
            ).first()

            if not contribution:
                return {"status": "error", "message": "Contribution not found"}

            # Create payment record
            payment = Payment(
                contribution_id=contribution_id,
                amount=intent.amount / 100,  # Convert from cents
                currency=intent.currency,
                payment_method=intent.payment_method_types[0],
                status="completed",
                transaction_id=intent.id,
                metadata=intent.metadata
            )
            self.db.add(payment)
            self.db.commit()

            # Update contribution status
            contribution.status = "completed"
            contribution.payment_id = payment.id
            self.db.commit()

            return {
                "status": "success",
                "message": "Payment processed successfully",
                "payment_id": payment.id
            }
        except stripe.error.StripeError as e:
            return {"status": "error", "message": str(e)}

    def get_payment_details(
        self,
        payment_id: int
    ) -> Dict[str, Any]:
        """Get payment details."""
        try:
            payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return {"status": "error", "message": "Payment not found"}

            return {
                "status": "success",
                "payment": {
                    "id": payment.id,
                    "amount": format_currency(payment.amount),
                    "currency": payment.currency,
                    "status": payment.status,
                    "payment_method": payment.payment_method,
                    "transaction_id": payment.transaction_id,
                    "created_at": payment.created_at.isoformat(),
                    "metadata": payment.metadata
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def refund_payment(
        self,
        payment_id: int,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Refund a payment."""
        try:
            payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return {"status": "error", "message": "Payment not found"}

            if payment.status != "completed":
                return {"status": "error", "message": "Payment not completed"}

            # Process refund through Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.transaction_id,
                reason=reason
            )

            # Update payment status
            payment.status = "refunded"
            payment.refund_id = refund.id
            payment.refunded_at = datetime.utcnow()
            self.db.commit()

            # Update contribution status
            contribution = payment.contribution
            contribution.status = "refunded"
            self.db.commit()

            return {
                "status": "success",
                "message": "Payment refunded successfully",
                "refund_id": refund.id
            }
        except stripe.error.StripeError as e:
            return {"status": "error", "message": str(e)}

    def get_payment_history(
        self,
        contribution_id: int
    ) -> Dict[str, Any]:
        """Get payment history for a contribution."""
        try:
            payments = self.db.query(Payment).filter(
                Payment.contribution_id == contribution_id
            ).order_by(Payment.created_at.desc()).all()

            return {
                "status": "success",
                "payments": [
                    {
                        "id": p.id,
                        "amount": format_currency(p.amount),
                        "currency": p.currency,
                        "status": p.status,
                        "payment_method": p.payment_method,
                        "transaction_id": p.transaction_id,
                        "created_at": p.created_at.isoformat(),
                        "refunded_at": p.refunded_at.isoformat() if p.refunded_at else None
                    }
                    for p in payments
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 