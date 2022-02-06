import os
from pathlib import Path
from loguru import logger


path = "C:\\Users\\Almaz\\Desktop\\Django_web_application_control-master"
out_put_path = str(Path.cwd())

# путь с которого запушен скрипт/exe/файл
print("working path:", Path.cwd())

# вывод всех элементов в указанной папке
print("все елементы папки:", os.listdir(out_put_path))




# обход папки с выводом пути и имени файла с расширением


# def obhodFile(path: str, level=1):
#     print("Level=", os.listdir(path))
# for i in os.listdir(path):
#   if os.path.isdir(path+"\\"+i):
#       print("Спускаемся", path+"\\"+i)
#       obhodFile(path+"\\"+i, level+1)
#       print("Возврашаемся в", path)


# obhodFile(out_put_path)

# проверка являтся ли папкой элемент
# for i in os.listdir(path):
#     print(path + "\\" + i, os.path.isdir(path + "\\" + i))


# WALK : В Т О Р О Й  В А Р И А Н Т
def find_file(name_path: str, file_name: str):
    """
    Поиск полного пути к нужному файлу, используя параметры name_path = имя_папки содержащей нужный файл 
    либо же другие подпапки содержащие искомый файл; file_name: имя искомого файла.
    Базовый путь начинается с пути выполняющегося скрипта или исполняемого файла
    """
    # --- Get all elements and find manage.py
    # out_put_path = str(Path.cwd())
    # list_elements = os.listdir(out_put_path)
    # element = "manage.py"
    # if element in list_elements:
    #     logger.info(f"element find")


    spisok = []
    out_put_path = str(Path.cwd())
    abs = os.path.abspath(__file__)
    # logger.info(f"текущая директория запус*ка 2: {abs}")
    logger.info(f"текущая директория запуска: {out_put_path}")

    for adress, dirs, files in os.walk(out_put_path + "\\" + name_path):
        for file in files:
            # print(file)

            full = os.path.join(adress, file)
            if file_name in full:
                # logger.info(f"xxx:{full}")
                spisok.append(full)
                print(f"Our spisok:\n", spisok)
                if len(spisok) == 1:
                    return spisok[0], abs
                elif len(spisok) > 1:
                    logger.warning("Found much files, we need a one file")
                elif len(spisok) == 0:
                    logger.warning(f"File not found in this path: ")


path_name = find_file(name_path="kovach", file_name="base")
print(f"path_name find: {path_name}")
