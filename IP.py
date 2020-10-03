
import sys
import argparse


def cli_network():
    '''
    Позволяет работать из командной строки
    '''
    network = argparse.ArgumentParser(
        prog = 'IP',
        description = '''Программа для нахождения минимальной подсети для заданного набора IP-адресов.''',
        add_help = False
    )
    network.add_argument('-f', '--file', required=True,
                         help='Имя файла с IP-адресами, задаётся в кавычках, например: "ipv4.txt"')
    network.add_argument('-v', '--version', required=True, help='Версия IP-протокола. 4 или 6')
    network.add_argument('--help', '-h', action='help', help='Справка')

    return network


def string_format(st, m):
    '''
    Дописывает в начале недостающее количество нулей в двоичной сиситеме.
    m - разрядность
    '''
    if len(str(st)) <= m-1:
        return str(0)*(m-len(str(st))) + str(st)
    else:
        return str(st)


def convert_ipv4(file):
    '''
    1. Среди имеющихся адресов ищет максимальный и минимальный.
    2. Передаёт их функции search_mask.
    '''
    max = str(0)
    min = str(1)*32
    bin_ip = ''
    num_str = 0
    str_in_error = []
    for ip in file: # каждый ip-адрес переводит в двоичную систему
        ip = ip.strip()
        byte = ip.split('.')
        num_str += 1
        for j in byte:
            if j.isdigit() and 0 <= int(j) <= 255:
                bin_ip += string_format(bin(int(j))[2:], 8)
            else:
                bin_ip = ''
                str_in_error.append(num_str)
                break
        if len(bin_ip) == 32:
            if int(bin_ip, 2) > int(max, 2): # ищет наиболее различные адреса
                max = bin_ip
            if int(bin_ip, 2) < int(min, 2):
                min = bin_ip
        else:
            continue
        bin_ip = ''
    search_mask(max, min, str_in_error)


def search_mask(max, min, str_in_error):
    '''
    1. Ищет маску подсети и префекс.
    2. Выводит результаты.
    '''
    m = 0
    for k in range(32):
        if max[k] == min[k]:
            m += 1
        else:
            break
    mask = str(1) * m + str(0) * (32 - m)
#    print(mask) # распечатывает маску подсети в бинарном формате
#    print(str(int(mask[:8], 2)) + '.' + str(int(mask[8:16], 2)) + '.' +
#        str(int(mask[16:24], 2)) + '.' + str(int(mask[24:], 2))) # распечатывает маску подсети
    subnet_bin = bin(int(max, 2) & int(mask, 2))[2:]
    if subnet_bin == '0' or subnet_bin == '1':
        subnet_bin = str(0) * 32
    subnet = 'Result net: ' + str(int(subnet_bin[:8], 2)) + '.' + str(int(subnet_bin[8:16], 2)) + '.' + \
             str(int(subnet_bin[16:24], 2)) + '.' + str(int(subnet_bin[24:], 2)) + '/' + str(m)

    return print(subnet), print('Результат выведен без учёта следующих строк:', *str_in_error)\
        if len(str_in_error) != 0 else print(subnet)


def start(name, version):
    '''
    Открывает фаил на чтение и запускает алгоритм.
    '''
    if version == '4':
        file = open(name, "r")
        convert_ipv4(file)
        file.close()
    elif version == '6':
        pass
    else:
        return print("Указана не правильная версия IP.", version)


if __name__ == "__main__":
    network = cli_network()
    namespace = network.parse_args(sys.argv[1:])
    start(namespace.file, namespace.version)

#start("IP_test.txt",4)
