Тестовое задание backend #1 (rest api Python)
Реализовать rest api:
- Имеется база пользователей (добавляются через админку/swagger, регистрацию делать не надо).
- У каждого пользователя при создании создается персональный блог. Новые создавать он не может.
- Пост в блоге — элементарная запись с заголовком, текстом (140 символов) и временем создания. Заголовок обязательное поле.
- Пользователь может подписываться/отписываться на блоги других пользователей (любое количество).
- У пользователя есть персональная лента новостей (не более ~500 постов), в которой выводятся посты из блогов, на которые он подписан, в порядке добавления постов.
