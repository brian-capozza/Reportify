from data_config import TABLE_DF
from Excel.Table import FormatRule, OperationRule, Table
from Excel.Workbook import Workbook


def main():
    wb = Workbook('file.xlsx', 'new')
    wb.new_sheet('Sales Data')

    table = Table('table', TABLE_DF, 'Sales Data', style=('dark', 'green', 'simple'), start_col=3, total_row='top')
    table.add_column_formats('units_sold', [FormatRule('redbg_bold_underline_twodecimal', '_column_ > 100'), FormatRule('yellowbg', '_column_ <= 100')])
    table.add_header_formats(TABLE_DF.columns, FormatRule('greenbg'))
    table.add_total_operation('product', OperationRule(['SUM', 'AVERAGE'], ['units_sold', 'revenue'], '/'))
    table.add_total_formats('product', FormatRule('bold'))
    wb.add_table(table)
    wb.extend_column_widths([15, 15, 15, 15, 15, 15, 15, 15], 2)

    wb.close()


if __name__ == "__main__":
    main()
