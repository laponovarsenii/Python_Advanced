from models import session, Category, Product

from db_connection import DBConnector, engine


from sqlalchemy import select, func
from models import Category, Product


with DBConnector(engine) as session:

    # electronics = Category(
    #     name="Электроника",
    #     description="Гаджеты и устройства."
    # )
    # books = Category(
    #     name="Книги",
    #     description="Печатные книги и электронные книги."
    # )
    # clothes = Category(
    #     name="Одежда",
    #     description="Одежда для мужчин и женщин."
    # )
    #
    # session.add_all([electronics, books, clothes])
    # session.commit()
    #

    # smartphone = Product(
    #     name="Смартфон",
    #     price=299.99,
    #     in_stock=True,
    #     category=electronics
    # )
    # laptop = Product(
    #     name="Ноутбук",
    #     price=499.99,
    #     in_stock=True,
    #     category=electronics
    # )
    # scifi_book = Product(
    #     name="Научно-фантастический роман",
    #     price=15.99,
    #     in_stock=True,
    #     category=books
    # )
    # jeans = Product(
    #     name="Джинсы",
    #     price=40.50,
    #     in_stock=True,
    #     category=clothes
    # )
    # tshirt = Product(
    #     name="Футболка",
    #     price=20.00,
    #     in_stock=True,
    #     category=clothes
    # )
    #
    # session.add_all([smartphone, laptop, scifi_book, jeans, tshirt])
    # session.commit()
    # print("Задача 1: данные добавлены\n")

    # =============================
    # Задача 2. Чтение данных
    # =============================

    print("Задача 2: категории и их продукты")

    stmt = select(Category)
    categories = session.execute(stmt).scalars()

    for category in categories:
        print(f"Категория: {category.name} — {category.description}")

        for product in category.products:
            print(f"  Продукт: {product.name}, цена: {product.price}")
        print("-" * 40)


    print("Задача 3: Обновление данных")
    # =============================
    # Задача 3. Обновление данных
    # =============================)

    stmt = (
        select(Product)
        .where(Product.name == "Смартфон")
        .limit(1)
    )
    smartphone_obj = session.execute(stmt).scalar_one_or_none()

    if smartphone_obj:
        smartphone_obj.price = 349.99
        session.commit()
        print("Цена 'Смартфон' обновлена до 349.99")
    else:
        print("Продукт 'Смартфон' не найден")


    print("Задача 4: Агрегация и группировка")
    # =============================
    # Задача 4. Агрегация и группировка
    # =============================


    stmt = (
        select(
            Category.name,
            func.count(Product.id).label("product_count")
        )
        .join(Product, Product.category_id == Category.id)
        .group_by(Category.id, Category.name)
    )
    result = session.execute(stmt).all()


    for row in result:
        print(f"Категория: {row.name}, продуктов: {row.product_count}")



    print("Задача 5: Группировка с фильтрацией")
    # =============================
    # Задача 5. Группировка с фильтрацией
    # =============================

    stmt = (
        select(
            Category.name,
            func.count(Product.id).label("product_count")
        )
        .join(Product, Product.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .having(func.count(Product.id) > 1)
    )

    result = session.execute(stmt).all()

    for row in result:
        print(f"Категория: {row.name}, продуктов: {row.product_count}")