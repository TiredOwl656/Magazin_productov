from datetime import datetime
from operator import itemgetter

# --- Данные ---
users_data = {}
products_data = [
    {'name': 'Молоко', 'price': 60, 'quantity': 10},
    {'name': 'Хлеб', 'price': 35, 'quantity': 20},
    {'name': 'Яйца', 'price': 80, 'quantity': 15}
]


def register_user():
    username = input("Введите имя пользователя: ")
    if username in users_data:
        print("Пользователь с таким именем уже существует. Выберите другое имя.")
        return
    while True:
        password = input("Введите пароль: ")
        confirm_password = input("Повторите пароль: ")
        if password == confirm_password:
            break
        else:
            print("Пароли не совпадают. Пожалуйста, повторите ввод.")
    while True:
        role = input("Роль (user/admin): ").lower()
        if role in ["user", "admin"]:
            break
        else:
            print("Неверная роль. Введите 'user' или 'admin'.")

    users_data[username] = {"password": password, "role": role, "cart": [], "history": []}
    print("Регистрация прошла успешно!")


def login():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    user = users_data.get(username)
    if user and user["password"] == password:
        return username, user["role"]
    else:
        print("Неверный логин или пароль. Пожалуйста, проверьте введенные данные.")
        return None, None


def add_product():
    name = input("Введите название товара: ")
    while True:
        try:
            price = float(input("Введите цену: "))
            if price <= 0:
                raise ValueError("Цена должна быть больше нуля.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите число больше 0.")
    while True:
        try:
            quantity = int(input("Введите количество: "))
            if quantity < 0:
                raise ValueError("Количество не может быть отрицательным.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите целое число больше или равное 0.")
    products_data.append({"name": name, "price": price, "quantity": quantity})
    print("Товар добавлен!")


def show_products(sorted_products=None):
    if not products_data:
        print("Товаров нет в наличии.")
        return

    products_to_display = sorted_products or products_data

    print("-" * 30)
    print("{:<20} {:<10} {:<10}".format("Название", "Цена", "Количество"))
    print("-" * 30)
    for i, product in enumerate(products_to_display):
        print(f"{i + 1}. {product['name']:<20} {product['price']:<10.2f} {product['quantity']:<10}")
    print("-" * 30)


def sort_products(products, sort_criteria):
    try:
        if sort_criteria == "price":
            return sorted(products, key=itemgetter('price'))
        elif sort_criteria == "price_desc":
            return sorted(products, key=itemgetter('price'), reverse=True)
        elif sort_criteria == "quantity":
            return sorted(products, key=itemgetter('quantity'))
        elif sort_criteria == "quantity_desc":
            return sorted(products, key=itemgetter('quantity'), reverse=True)
        elif sort_criteria == "name":
            return sorted(products, key=lambda x: x['name'].lower())
        elif sort_criteria == "name_desc":
            return sorted(products, key=lambda x: x['name'].lower(), reverse=True)
        else:
            return products
    except KeyError as e:
        print(f"Ошибка сортировки:  Ключ '{e}' не найден в данных продукта.")
        return products


def manage_users():

    print_users_list()

    while True:
        print("\nВыберите действие: ")
        print("1 - добавить пользователя")
        print("2 - изменить роль пользователя")
        print("3 - изменить пароль пользователя")
        print("4 - удалить пользователя")
        print("5 - назад")
        action = input()
        try:
            if action == '1':
                register_user()
            elif action == '2':
                change_user_role()
            elif action == '3':
                change_user_password()
            elif action == '4':
                delete_user()
            elif action == '5':
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def delete_user():

    print_users_list()

    try:
        user_index = int(input("Введите номер пользователя для удаления: ")) - 1
        if 0 <= user_index < len(users_data):
            username_to_delete = list(users_data.keys())[user_index]
            del users_data[username_to_delete]
            print(f"Пользователь {username_to_delete} удален.")
        else:
            print("Неверный номер пользователя.")
    except ValueError:
        print("Неверный формат ввода. Пожалуйста, введите число.")
    except IndexError:
        print("Пользователь с таким номером не найден.")


def change_user_role():

    print_users_list()

    try:
        user_index = int(input("Введите номер пользователя для изменения роли: ")) - 1
        if 0 <= user_index < len(users_data):
            username_to_change = list(users_data.keys())[user_index]
            new_role = input("Введите новую роль (user/admin): ").lower()
            if new_role in ["user", "admin"]:
                users_data[username_to_change]["role"] = new_role
                print(f"Роль пользователя {username_to_change} изменена на {new_role}.")
            else:
                print("Неверная роль. Введите 'user' или 'admin'.")
        else:
            print("Неверный номер пользователя.")
    except ValueError:
        print("Неверный формат ввода. Пожалуйста, введите число.")
    except IndexError:
        print("Пользователь с таким номером не найден.")


def add_to_cart(username):
    show_products()
    try:
        product_index = int(input("Введите номер товара: ")) - 1
        if 0 <= product_index < len(products_data):
            product = products_data[product_index].copy()
            if product["quantity"] > 0:
                if product not in users_data[username]["cart"]:
                    users_data[username]["cart"].append(product)
                    products_data[product_index]["quantity"] -= 1
                    print("Товар добавлен в корзину!")
                else:
                    print("Товар уже в корзине")
            else:
                print("Товар отсутствует на складе.")
        else:
            print("Неверный номер товара.")
    except (ValueError, IndexError) as e:
        print(f"Ошибка: {e}. Пожалуйста, проверьте введенный номер товара.")
    except KeyError as e:
        print(f"Ошибка: {e}. Пользователь не найден.")


def view_cart(username):
    cart = users_data[username]["cart"]
    if not cart:
        print("Корзина пуста.")
        return

    while True:
        print("\nСортировка корзины:")
        print("1. Сортировать по цене (по возрастанию)")
        print("2. Сортировать по цене (по убыванию)")
        print("3. Сортировать по количеству (по возрастанию)")
        print("4. Сортировать по количеству (по убыванию)")
        print("5. Сортировать по названию (A-Я)")
        print("6. Сортировать по названию (Я-А)")
        print("7. Не сортировать")
        sort_choice = input("Выберите способ сортировки: ")
        if sort_choice in ["1", "2", "3", "4", "5", "6", "7"]:
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 7.")

    if sort_choice == "1":
        sorted_cart = sort_products(cart, "price")
    elif sort_choice == "2":
        sorted_cart = sort_products(cart, "price_desc")
    elif sort_choice == "3":
        sorted_cart = sort_products(cart, "quantity")
    elif sort_choice == "4":
        sorted_cart = sort_products(cart, "quantity_desc")
    elif sort_choice == "5":
        sorted_cart = sort_products(cart, "name")
    elif sort_choice == "6":
        sorted_cart = sort_products(cart, "name_desc")
    else:
        sorted_cart = cart

    total_cost = sum(product["price"] for product in cart)
    print("-" * 30)
    print("{:<20} {:<10}".format("Название", "Цена"))
    print("-" * 30)
    for product in sorted_cart:
        print("{:<20} {:<10.2f}".format(product["name"], product["price"]))
    print("-" * 30)
    print(f"Итоговая стоимость: {total_cost:.2f}")


def checkout(username):
    view_cart(username)
    if input("Подтвердить покупку? (y/n): ").lower() == "y":
        for product in users_data[username]["cart"]:
            product['purchase_date'] = datetime.now().isoformat()
        users_data[username]["history"].extend(users_data[username]["cart"])
        users_data[username]["cart"] = []
        print("Покупка завершена!")
    else:
        print("Покупка отменена.")


def show_purchase_history(username):
    history = users_data[username].get('history', [])
    if not history:
        print("История покупок пуста.")
        return

    print("\nИстория покупок:")
    for i, purchase in enumerate(history):
        print(f"--- Покупка {i + 1} ---")
        print(f"Название: {purchase['name']}")
        print(f"Цена: {purchase['price']:.2f}")
        print(f"Дата покупки: {purchase['purchase_date']}")
        print("-" * 20)


def delete_product():
    while True:
        print("\nУдаление товара:")
        print("1. Удалить товар по названию")
        print("2. Назад")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                product_name = input("Введите название товара: ")
                products_data[:] = [p for p in products_data if p["name"] != product_name]
                print(f"Товар '{product_name}' удален.")
                break
            elif choice == "2":
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Ошибка при удалении товара: {e}")


def manage_product():
    while True:
        print("\nРедактирование данных:")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Изменить информацию о товаре")
        print("4. Назад")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                add_product()
            elif choice == "2":
                delete_product()
            elif choice == "3":
                edit_product()
            elif choice == "4":
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Ошибка в меню управления товарами: {e}")


def edit_product():
    show_products()
    try:
        product_index = int(input("Введите номер товара для редактирования: ")) - 1
        if 0 <= product_index < len(products_data):
            product = products_data[product_index]
            product["name"] = input(f"Новое название товара ({product['name']}): ") or product["name"]
            while True:
                try:
                    new_price = input(f"Новая цена товара ({product['price']}): ")
                    product["price"] = float(new_price) if new_price else product["price"]
                    if product["price"] <= 0:
                        raise ValueError("Цена должна быть больше нуля.")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e}. Пожалуйста, введите число больше 0.")
            while True:
                try:
                    new_quantity = input(f"Новое количество товара ({product['quantity']}): ")
                    product["quantity"] = int(new_quantity) if new_quantity else product["quantity"]
                    if product["quantity"] < 0:
                        raise ValueError("Количество не может быть отрицательным.")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e}. Пожалуйста, введите целое число больше или равное 0.")
            print("Товар успешно отредактирован.")
        else:
            print("Неверный номер товара.")
    except (ValueError, IndexError) as e:
        print(f"Ошибка при редактировании товара: {e}")


def edit_user():

    print_users_list()

    try:
        user_index = int(input("\nВведите номер пользователя для редактирования: ")) - 1
        if 0 <= user_index < len(users_data):
            username_to_edit = list(users_data.keys())[user_index]
            new_role = input(
                f"Новая роль для пользователя {username_to_edit} ({users_data[username_to_edit]['role']}): ").lower()
            if new_role in ["user", "admin"]:
                users_data[username_to_edit]["role"] = new_role
                print(f"Роль пользователя {username_to_edit} изменена на {new_role}")
            else:
                print("Неверная роль.")
        else:
            print("Неверный номер пользователя.")
    except ValueError:
        print("Неверный формат ввода.")
    except KeyError:
        print("Ошибка доступа к данным пользователя.")


def print_users_list():
    
    if not users_data:
        print("Нет зарегистрированных пользователей.")
        return

    print("\nСписок пользователей:")
    for i, (username, user_data) in enumerate(users_data.items()):
        print(f"{i + 1}. Имя пользователя: {username}, Роль: {user_data['role']}")


def show_statistics():
    total_purchases = 0
    total_revenue = 0
    for username, user_data in users_data.items():
        for purchase in user_data.get("history", []):
            total_purchases += 1
            total_revenue += purchase["price"]

    if total_purchases > 0:
        average_purchase_value = total_revenue / total_purchases
        print(f"\nСтатистика:")
        print(f"Общее количество покупок: {total_purchases}")
        print(f"Общая выручка: {total_revenue:.2f}")
        print(f"Средняя стоимость покупки: {average_purchase_value:.2f}")
    else:
        print("\nСтатистика пока недоступна (нет покупок).")


def change_user_password():

    print_users_list()

    try:
        user_index = int(input("\nВведите номер пользователя для изменения пароля: ")) - 1
        if 0 <= user_index < len(users_data):
            username_to_change = list(users_data.keys())[user_index]
            while True:
                new_password = input(f"Введите новый пароль для пользователя {username_to_change}: ")
                confirm_password = input(f"Повторите новый пароль для пользователя {username_to_change}: ")
                if new_password == confirm_password:
                    break
                else:
                    print("Пароли не совпадают. Пожалуйста, повторите ввод.")
            users_data[username_to_change]["password"] = new_password
            print(f"Пароль пользователя {username_to_change} успешно изменен.")
        else:
            print("Неверный номер пользователя.")
    except ValueError:
        print("Неверный формат ввода. Пожалуйста, введите число.")
    except KeyError:
        print("Ошибка доступа к данным пользователя.")


def user_menu(username):
    while True:
        print("\nМеню пользователя:")
        print("1. Просмотреть товары")
        print("2. Добавить в корзину")
        print("3. Просмотреть корзину")
        print("4. Оформить заказ")
        print("5. История покупок")
        print("6. Выйти")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                while True:
                    print("\nСортировка товаров:")
                    print("1. Сортировать по цене (по возрастанию)")
                    print("2. Сортировать по цене (по убыванию)")
                    print("3. Сортировать по количеству (по возрастанию)")
                    print("4. Сортировать по количеству (по убыванию)")
                    print("5. Сортировать по названию (A-Я)")
                    print("6. Сортировать по названию (Я-А)")
                    print("7. Не сортировать")
                    sort_choice = input("Выберите способ сортировки: ")
                    if sort_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                        break
                    else:
                        print("Неверный выбор. Пожалуйста, выберите число от 1 до 7.")

                sorted_products = None
                if sort_choice == "1":
                    sorted_products = sort_products(products_data, "price")
                elif sort_choice == "2":
                    sorted_products = sort_products(products_data, "price_desc")
                elif sort_choice == "3":
                    sorted_products = sort_products(products_data, "quantity")
                elif sort_choice == "4":
                    sorted_products = sort_products(products_data, "quantity_desc")
                elif sort_choice == "5":
                    sorted_products = sort_products(products_data, "name")
                elif sort_choice == "6":
                    sorted_products = sort_products(products_data, "name_desc")

                show_products(sorted_products)

            elif choice == "2":
                add_to_cart(username)
            elif choice == "3":
                view_cart(username)
            elif choice == "4":
                checkout(username)
            elif choice == "5":
                show_purchase_history(username)
            elif choice == "6":
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def admin_menu():
    while True:
        print("\nМеню администратора:")
        print("1. Просмотреть товары")
        print("2. Управление пользователями")
        print("3. Управление товаром")
        print("4. Просмотр статистики")
        print("5. Выйти")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_products()
            elif choice == "2":
                manage_users()
            elif choice == "3":
                manage_product()
            elif choice == "4":
                show_statistics()
            elif choice == "5":
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Произошла ошибка в меню администратора: {e}")


while True:
    print("\nМеню:")
    print("1. Регистрация")
    print("2. Вход")
    print("3. Выход")

    choice = input("Выберите действие: ")
    try:
        if choice == "1":
            register_user()
        elif choice == "2":
            username, role = login()
            if username:
                if role == "admin":
                    admin_menu()
                elif role == "user":
                    user_menu(username)
        elif choice == "3":
            break
        else:
            print("Неверный выбор.")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")