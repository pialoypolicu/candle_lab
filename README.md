endpoints

- catalog/
- purchase/
- arrival/
- instock/
- production/

#### catalog/
энд пойнт Для создания записей материала, который можно купить/заказать

get method возвращает список всех записей из таблицы

post method создает новую запись в таблице

Передаваемая data post запроса:

- name: str
- volume: int
- company: str

example {"name": "wax", "volume": 30, "company": "black"}

#### purchase/
Эндпойнт который регистрирует покупку материала, выдает историю закупок и можно выборочно по индексу выбирать закупку

Оформляя зааказ, каждый раз создается новая запись в таблице purchase. 

При создании записи, по дефолту ставится статус в arrrival WAY - on the way

С получением и отметкой о поступлении товара, статус arrival изменится на ARR - arrived

get method:

- purchase/ выдает весь список, без пагинации
- purchase/<int:> выдает одну запись

post method:

purchase/

- catalog_name **automaticaly required**
- name: str **required**
- volume: int **required**
- company: str **required**
- date_purchase: str ex: 2022-04-01 **required**
- quantity: int **required**
- price: int **required** 
- comment: str | None **null=True**
- arrival: int **null=True**

example {"date_purchase": "2022-01-01", "quantity": 1, "volume": 30, "price": 777, "comments": "Hello", "arrival": 1}

arrival/
-
Эндпойнт для фиксации прибытия товара/материала.

После его поступления, будет запись в таблице InStock.

Если записи нет, то будет создана, если запись ранее была, то будет обновление.

###_Характеристики функционала arrival_:

- name поле уникальное
- quantity, значение поля количество заказанных позиций товара/материала. Если поле не передано, то по умолчанию будет 
применено значение один.
Если заказано несколько единиц одной каталожной позиции, то quantity уиножается на единицу измерения, заказанной позиции.

#### arrival/

выдает список всех позиций в таблице Instock

#### post method
arrival/

data:
- name: str required
- quantity: int required
- volume: int required

example {"name": "wax-1", "volume": 30, "quantity": 2}


#### instock/ get method

выдает весь список наличия товара на складе

#### arrival/{pk: int}/ get method

Выдает один объект из таблицы Instock


#### production/

Эндппойнт для изменения позиций после изготовления продукта

Покрытие тестами:

TODO
Остановился с работой production. нужно начать реализацию изменения записей в instock