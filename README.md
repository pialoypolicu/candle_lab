endpoints

- catalog/
- purchase/
- pin-result/
- arrival-instock/

#### catalog/
энд пойнт Для создания записей материала, который можно купить/заказать

get method возвращает список всех записей из таблицы

post methhod создает новую запись в таблице

Передаваемая data post запроса:

- name: str
- weight: int
- company: str

example {"name": "wax", "weight": 30, "company": "black"}

#### purchase/
Эндпойнт который регистрирует покупку материала, выдает историю закупок и можно выборочно по индексу выбирать закупку

Сперва создаем запись в таблице закупки Purchase.

Если запись создана успешно, то следующий шаг создаем запись в таблице ArrivalWait. 
Таблица хранит в себе записи ождиаемых покупок

get method:

- purchase/ выдает весь список, без пагинации
- purchase/<int:> выдает одну запись

post method:

purchase/

- catalog_name: int
- date_purchase: str
- quantity: int
- weight: int
- price: int
- comments: str | None

example {"catalog_name": 1, "date_purchase": "2022-01-01", "quantity": 1, "weight": 30, "price": 777, "comments": "Hello"}
