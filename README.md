endpoints

- catalog/
- purchase/
- arrival/

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

при создании записи, по дефолту ставится статус в arrrival WAY - on the way

С получением и отметкой о поступлении товара, статус arrival изменится на ARR - arrived

get method:

- purchase/ выдает весь список, без пагинации
- purchase/<int:> выдает одну запись

post method:

purchase/

- catalog_name: int
- date_purchase: str
- quantity: int
- volume: int
- price: int
- comment: str | None
- arrival: int

example {"catalog_name": 1, "date_purchase": "2022-01-01", "quantity": 1, "volume": 30, "price": 777, "comments": "Hello", "arrival": 1}

arrival/
-
Эндпойнт для отметки пррибытия товара.

После его поступления, будет запись в таблице InStock запись.

Если записи нет, то будет создана, если запись ранее была, то будет обновление.

#### post method

data-
- name: str
- volume: int

example {"name": "wax-1", "volume": 30}

Покрытие тестами:
- проверка создания записи в InStock
- реализовать проверрку обновления записи в InStock

Нужно реализовать обновление записи в InStock, если такая запись уже была создана.
