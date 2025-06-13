from apps.catalogo.models import Item


class ItemDomain:
    def __init__(self, item: Item):
        self.item = item

    @staticmethod
    def instance_by_item(item_id: int) -> 'ItemDomain':
        item = Item.objects.get(id=item_id)
        return ItemDomain(
            item=item
        )