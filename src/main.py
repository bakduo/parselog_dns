#!/usr/bin/python3


"""
Permite realizar un reporte de tres variantes diferentes. La salida del reporte
es por medio de ip únicas o por medio de grupo de redes solo en dos casos puntuales.
Los rangos de subredes deben de ser completados según la necesidad del reporte
"""

from generate_report import GenerateClassic, GenerateNXDOMAIN, GenerateTimeout

reportes = []

reportes.append(GenerateClassic())
reportes.append(GenerateNXDOMAIN())
reportes.append(GenerateTimeout())


if __name__ == "__main__":
    for report in reportes:
        report.set_filelog("dns.log")
        report.exec_cmd()