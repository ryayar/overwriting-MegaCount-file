from ftplib import FTP
import datetime
import os

directory = "C:\\MegaCount"  # начальная директория, откуда брать файл с видом "НомерСчетчика_Год-Месяц-День"
dt = str(datetime.date.today() - datetime.timedelta(days=1))
ftp_serv = 'ftp.ftp.ru'
ftp_login = 'ftp_login'
ftp_pass = 'ftp_pass'
ftp_path = 'ftp_path'
spliter = '-' * 50


def download_file():
    with FTP(ftp_serv, ftp_login, ftp_pass) as ftp:
        ftp.cwd(ftp_path)
        filenames = ftp.nlst() #загоняем в переменную filenames список содержимого директории
        for filename in filenames:
            list_split = filename.split('_')
            host_file = os.path.join(directory, filename)
            if list_split[0] == '063163001' and list_split[-1] == dt:
                try:
                    with open(host_file, 'wb') as local_file:
                        ftp.retrbinary('RETR %s' % filename, local_file.write)
                    file_found = True
                except:
                    pass
                if file_found:
                    ftp.delete(filename)


def overwriting_file():
    files_old_directory = os.listdir(directory) # чтение элементов в основной директории
    for old_file in files_old_directory:
        file = os.path.isfile(directory + "\\" + old_file)
        if file:
            time = old_file.split('_')
            time = time[-1].split('-')
            new_file_name = f'DB{time}.csv'
            with open(f'{directory}\\{old_file}', 'r+', encoding='UTF-8') as oldfile:
                with open(f'{directory}\\new\\{new_file_name}', 'w+', encoding='UTF-8') as newfile:
                    newfile.write('TIME;IN;OUT;OVERLAP\n')  # первая строчка всегда имеет "TIME;IN;OUT;OVERLAP\n"
                    lines = oldfile.readlines()  # смотрим все строчки из старого файла
                    for line in lines:  # построчно обходит старый файл
                        try:
                            line = line.strip().split(' ')
                            newfile.writelines(f'{line[0]};{line[1]};{line[2]};TRUE\n')
                        except:
                            pass
            os.replace(f'{directory}\\{old_file}', f'{directory}\\old\\{old_file}') # перемещает исходный файл в новую директорию


def upload_file():
    with FTP(ftp_serv, ftp_login, ftp_pass) as ftp:
        ftp.cwd(ftp_path)
        dir = 'C:\\MegaCount\\new\\'
        file_dir = os.listdir(dir)[-1]
        upload_file = open(f'{dir + file_dir}', 'rb')
        ftp.storbinary('STOR ' + file_dir, upload_file)


def main():
    download_file()
    download_file()
    upload_file()


if __name__ == "__main__":
    main()