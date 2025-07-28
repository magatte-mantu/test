# SQL Query Generator from Excel Mapping

This tool automatically generates a SQL SELECT query from an Excel file. It is designed to simplify SQL writing, especially for analysts or developers working with SQL Server (Azure Data Studio compatible).

## 🔧 How it works

You provide a mapping Excel file (`mapping.xlsx`) with:

### A. Selected columns (columns A to C)

| alias (Excel) | column (SQL) | table   |
| ------------- | ------------ | ------- |
| client\_name  | name         | clients |
| order\_date   | date         | orders  |

### B. Join definitions (columns G to H)

| join\_from        | join\_to   |
| ----------------- | ---------- |
| orders.client\_id | clients.id |

## ▶️ How to use

1. Install dependencies:

```bash
pip install pandas openpyxl
```

2. Make sure your Excel file is named `mapping.xlsx` and placed in the same folder as the script.

3. Run the script:

```bash
python sql-generator.py
```

4. The SQL query will be generated in a file called `query.txt` in the same folder.

## 📄 Output example

```sql
SELECT
    clients.name AS client_name,
    orders.date AS order_date
FROM
    orders
JOIN clients ON orders.client_id = clients.id
```

## ✅ Notes

* The script automatically chooses the most relevant main table.
* Empty rows or incomplete joins are ignored.
