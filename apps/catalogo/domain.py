from apps.catalogo.models import Item, ItemFabricante, Fabricante


class ItemFabricanteDomain:
    def __init__(self, itemfabricante: ItemFabricante):
        self.itemfabricante = itemfabricante

    @staticmethod
    def instance_by_itemfabricante(itemfabricante_id: int) -> 'ItemFabricanteDomain':
        itemfabricante = ItemFabricante.objects.get(id=itemfabricante_id)
        return ItemFabricanteDomain(itemfabricante)

    def get_item_fabricante(self):
        return ItemFabricante.objects.get(id=self.itemfabricante.id)

    def get_item(self):
        item_fabricante = ItemFabricante.objects.get(id=self.itemfabricante.id)
        return Item.objects.get(id=item_fabricante.item.id)

    def get_fabricante(self):
        item_fabricante = ItemFabricante.objects.get(id=self.itemfabricante.id)
        return Fabricante.objects.get(id=item_fabricante.fabricante.id)

class ItemDomain:
    def __init__(self, item: Item):
        self.item = item

    @staticmethod
    def instance_by_item(item_id: int) -> 'ItemDomain':
        item = Item.objects.get(id=item_id)
        return ItemDomain(
            item=item
        )


