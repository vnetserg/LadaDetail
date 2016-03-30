# -*- coding: utf-8 -*-

import datetime, random, subprocess
from PyQt5.QtSql import QSqlQuery

def report_day_sales(for_date, file, dbase):
    query = QSqlQuery("SELECT shop.name AS name, sum(order_detail.quantity) AS qnt, sum(detail.price * order_detail.quantity) AS price \
        FROM shop INNER JOIN orders ON shop.id = orders.shop_id \
        INNER JOIN order_detail ON order_detail.order_id = orders.id \
        INNER JOIN detail ON detail.id = order_detail.detail_id \
        WHERE orders.regdate = \"{}\"\
        GROUP BY shop.name".format(for_date.toString("yyyy.MM.dd")), dbase)
    if not query.isActive():
        return print(query.lastError().text())
    with open("reports/goods.html", "r") as f:
        html = f.read()
    rows = []
    qnt_total = 0
    price_total = 0
    while query.next():
        rows.append("<tr><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(
            query.value("name"), int(query.value("qnt")), int(query.value("price"))))
        qnt_total += int(query.value("qnt"))
        price_total = int(query.value("price"))
    rows.append("<b><tr><td align='right'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr></b>".format(
        "Итого:", qnt_total, price_total))
    date = datetime.date.today().strftime("%d.%m.%Y")
    html = html.format(for_day = for_date.toString("dd.MM.yyyy"), date = date, rows = "\n".join(rows))
    tmpfile = "/tmp/report{}.html".format(random.randrange(1000000))
    with open(tmpfile, "w") as f:
        f.write(html)
    subprocess.call(["wkhtmltopdf", tmpfile, file])

def report_month_sales(file, dbase):
    for_date = date = datetime.date.today()
    query = QSqlQuery("SELECT employee.firstname AS firstname, employee.lastname AS lastname, employee.middlename AS middlename, \
            count(orders.id) AS qnt, sum(orders.price) AS price \
        FROM employee INNER JOIN orders ON employee.id = orders.employee_id \
        WHERE orders.regdate >= \"{}\"\
        GROUP BY employee.firstname, employee.lastname, employee.middlename".format(for_date.strftime("%Y.%m.01")), dbase)
    if not query.isActive():
        return print(query.lastError().text())
    with open("reports/emp_sales.html", "r") as f:
        html = f.read()
    rows = []
    qnt_total = 0
    price_total = 0
    while query.next():
        rows.append("<tr><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(
            "{} {}. {}.".format(query.value("lastname"), query.value("firstname")[0], query.value("middlename")[0]),
            int(query.value("qnt")), int(query.value("price"))))
        qnt_total += int(query.value("qnt"))
        price_total = int(query.value("price"))
    rows.append("<b><tr><td align='right'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr></b>".format(
        "Итого:", qnt_total, price_total))
    date = datetime.date.today().strftime("%d.%m.%Y")
    html = html.format(for_month = for_date.strftime("%m.%Y"), date = date, rows = "\n".join(rows))
    tmpfile = "/tmp/report{}.html".format(random.randrange(1000000))
    with open(tmpfile, "w") as f:
        f.write(html)
    subprocess.call(["wkhtmltopdf", tmpfile, file])