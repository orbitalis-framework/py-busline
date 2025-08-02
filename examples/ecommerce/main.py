import asyncio

from examples.ecommerce.ai_model import AIModel
from examples.ecommerce.backend import EcommerceBackend
from examples.ecommerce.data_processor import DataProcessor
from examples.ecommerce.email_sender import ConfirmationEmailSender
from examples.ecommerce.order import Product
from examples.ecommerce.supplier_notifier import SupplierNotifier


async def main():

    # Initialize components
    supplier_notifier = SupplierNotifier()
    email_sender = ConfirmationEmailSender()
    data_processor = DataProcessor()
    ai_model = AIModel()
    backend = EcommerceBackend()

    # Start them in order to execute `subscribe` method
    await asyncio.gather(
        supplier_notifier.start(),
        email_sender.start(),
        data_processor.start(),
        ai_model.start(),
        backend.start(),
    )

    user = "john.doe@email.com"

    backend.login(user)     # sync call to log the user

    backend.add_to_cart(Product("Keyboard", 49.99))
    backend.add_to_cart(Product("Mouse", 19.99))

    await backend.buy()     # create and send a new order composed by products in chart

    await asyncio.sleep(3)  # release eventloop in favor of other components


if __name__ == '__main__':
    asyncio.run(main())


