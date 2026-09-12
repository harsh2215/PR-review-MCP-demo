from src.services.payment_service import PaymentService


class PaymentController:
    def __init__(self, payment_service: PaymentService) -> None:
        self._payment_service = payment_service

    def create_payment(self, user_id: str, amount: float, currency: str):
        return self._payment_service.create_payment(user_id, amount, currency)

    def get_payment(self, payment_id: str):
        return self._payment_service.get_payment(payment_id)

    def update_payment_status(self, payment_id: str, status: str):
        return self._payment_service.update_payment_status(payment_id, status)
