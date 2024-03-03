


class Product():
    """
    Class representing a product.

    Attributes:
        id (str): Unique identifier of the product.
        name (str): Product name.
        description (str): Product description.
        price (float): Price of the product.
        stock (int): Quantity available in stock of the product.
        category (str): Product category.
        category_id (str): Unique identifier of the product category.
        created_at (datetime): Date and time of product creation.
        updated_at (datetime): Date and time of the last update of the product.
    """

    def __init__(self, **kwargs):
        """
        Initializes an object of type Product.

        Args:
            **kwargs: key-value arguments to initialize product attributes.
        """
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.price = kwargs.get('price')
        self.stock = kwargs.get('stock')
        self.category = kwargs.get('category')
        self.category_id = kwargs.get('category_id')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')

    def to_dict(self):
        """
        Returns a dictionary with the product attributes in a serializable format.

        Returns:
            dict: Dictionary with the product attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
