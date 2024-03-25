import mercadopago
import os


class MP_SDK():
    """
    MP_Services class.

    This class that provides access to the Mercado Pago SDK.
    It initializes the SDK with the provided access token.

    Attributes:
        sdk (mercadopago.SDK): The instance of the Mercado Pago SDK.

    Methods:
        __init__(self): Initializes the MP_Services class and the Mercado Pago SDK.

    """

    def __init__(self):
        self.sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))
