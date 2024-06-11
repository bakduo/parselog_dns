import os
   
from abc import ABC, abstractmethod

import logging

from ipaddress import IPv4Address, IPv4Network

SUBNET=['192.168.100.0',
        '172.16.10.0',
        '192.168.200.0']

def generarte_network():
    subnet_list = []
    for net in SUBNET:
        subnet_list.append(IPv4Network((net, "255.255.255.0")))
    return subnet_list

def check_ip_subnet(ip,network):

    check_ip = None
    try:
       check_ip = IPv4Address(ip)
       name_net = None
       for net in network:
           if check_ip in list(net.hosts()):
               name_net = net
               break

       return name_net

    except Exception as e:
        logging.debug("check_ip_subnet an error occurred: {} para la IP: {}".format(e,ip))

    return None


def imprimir_reporte_by_group(networks,input_csv,output_csv,):

    reporte_ip = open(output_csv,'w')
    
    filecsv = input_csv
    
    try:
        dict_networks = {}
        with open(filecsv) as fpin:
            for nr, line in enumerate(fpin):
                cadena = line.strip()
                cantidad, ip = cadena.split(',')
                name_net = check_ip_subnet(ip,networks)
                if name_net != None:
                    try:
                        if (dict_networks[str(name_net)]):
                            dict_networks[str(name_net)] = int(dict_networks[str(name_net)]) + int(cantidad)
                    except KeyError as e:
                        dict_networks[str(name_net)] = int(cantidad)


        for name,value in dict_networks.items():
            #logging.debug("{} total: {}".format(name,value))
            reporte_cadena = "{},{}\n".format(value,name)
            reporte_ip.write(reporte_cadena)

    finally:
        reporte_ip.close()



def imprimir_reporte_by_ip(input_csv,output):

    reporte_ip = open(output,'w')

    filecsv = input_csv

    try:
        with open(filecsv) as fpin:
            for nr, line in enumerate(fpin):
                cadena = line.strip()
                dim = len(cadena.split(','))
                cantidad = int(cadena.split(',')[dim-2])
                ip = cadena.split(',')[dim-1]
                reporte_cadena = "{},{}\n".format(cantidad,ip)
                reporte_ip.write(reporte_cadena)
    finally:
        reporte_ip.close()

class GenerateReport(ABC):

    @abstractmethod
    def exec_cmd(self):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        return hasattr(C, "exec_cmd")

class GenerateNXDOMAIN(GenerateReport):

    def __init__(self):
        super().__init__()
        self.filelog = ""
        self.output = "cantidad_totales_dns_nxdomain.txt"
        self.output_csv = "reporte_nxdomain.csv"
        self.output_group_csv = "reporte_by_group_nxdomain.csv"
        self.admin = False

    def set_filelog(self,name):
        self.filelog = name

    def switch_admin(self):
        self.admin = True

    def exec_cmd(self):
        try:
            if (self.admin):
                cmd1 = "sudo cat {}".format(self.filelog)
            else:
                cmd1 = "cat {}".format(self.filelog)

            comando1 = cmd1 + "|grep -iv 'linux/amd64, go' | grep -iv 'plugin/file' | grep -iv 'plugin/transfer'| grep -vi timeout | grep NXDOMA | awk '{print $2}' | cut -d':' -f 1 | sort | uniq -c | sort -rn | sed -re 's/ /,/g' > cantidad_totales_dns_nxdomain.txt"
            os.system(comando1)
            imprimir_reporte_by_ip(self.output,self.output_csv)
            redes = generarte_network()
            imprimir_reporte_by_group(redes,self.output_csv,self.output_group_csv)
            return True
        except Exception as e:
            print("An error occurred:", e)
        return False
    
class GenerateTimeout(GenerateReport):

    def __init__(self):
        super().__init__()
        self.filelog = ""
        self.output = "cantidad_totales_dns_timeout.txt"
        self.output_csv = "reporte_timeout.csv"
        self.admin = False

    def set_filelog(self,name):
        self.filelog = name

    def switch_admin(self):
        self.admin = True

    def exec_cmd(self):
        try:
            if (self.admin):
                cmd1 = "sudo cat {}".format(self.filelog)
            else:
                cmd1 = "cat {}".format(self.filelog)

            comando1 = cmd1 + "|grep -iv 'linux/amd64, go' | grep -iv 'plugin/file' | grep -iv 'plugin/transfer'| grep timeout | grep ERROR | awk '{print $4}' | sort | uniq -c | sort -rn |  sed -re 's/ /,/g' > cantidad_totales_dns_timeout.txt"
            os.system(comando1)
            imprimir_reporte_by_ip(self.output,self.output_csv)

            return True
        except Exception as e:
            logging.debug("An error occurred:", e)

        return False
    
class GenerateClassic(GenerateReport):

    def __init__(self):
        super().__init__()
        self.filelog = ""
        self.output = "cantidad_totales_dns.txt"
        self.output_csv = "reporte.csv"
        self.output_group_csv = "reporte_by_group.csv"
        self.cmd_admin = "sudo"
        self.admin = False

    def set_filelog(self,name):
        self.filelog = name

    def switch_admin(self):
        self.admin = True

    def exec_cmd(self):
        try:
            if (self.admin):
                cmd1 = "sudo cat {}".format(self.filelog)
            else:
                cmd1 = "cat {}".format(self.filelog)
                
            comando1 = cmd1 + "|grep -iv 'linux/amd64, go' | grep -iv 'plugin/file' | grep -iv 'plugin/transfer'| grep -iv timeout | awk '{print $2}' | cut -d':' -f 1 | sort | uniq -c | sort -rn | sed -re 's/ /,/g' > cantidad_totales_dns.txt"
            os.system(comando1)
            imprimir_reporte_by_ip(self.output,self.output_csv)
            redes = generarte_network()
            imprimir_reporte_by_group(redes,self.output_csv,self.output_group_csv)

            return True
        except Exception as e:
            logging.debug("An error occurred:", e)

        return False