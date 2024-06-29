def write_text_to_file(data, filename = "file.txt"):
    text = data.to_string()
    # Открытие файла в режиме записи и запись текста
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Текст успешно записан в {filename}")