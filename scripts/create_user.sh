uv run python -m scripts.create_user --username ab --password 12 --role administrator --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email anthocyane@yandex.ru --phone_number +79642501607

uv run python -m scripts.create_user --username a --password 12 --role student --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email pavel.seko4@gmail.com --phone_number +79642501606 --points 200

# Для добавления в группу:

uv run python -m scripts.create_user --username a --password 12 --role student --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email pavel.seko4@gmail.com --phone_number +79642501606 --points 200 --group_id 123e4567-e89b-12d3-a456-426614174000