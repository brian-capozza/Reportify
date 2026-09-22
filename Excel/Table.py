import collections
from dataclasses import dataclass
from typing import Literal

import pandas as pd

TableTier = Literal["light", "medium", "dark"]
TableColor = Literal["blue", "red", "green", "purple", "orange", "gray"]
TableVariant = Literal["simple", "outline", "clean"]

Operation = Literal['*', '/', '+', '-']

AGG_CONVERSION = {'AVERAGE': 1,
                  'COUNT': 2,
                  'COUNTA': 3,
                  'MAX': 4,
                  'MIN': 5,
                  'PRODUCT': 6,
                  'STDEV.S': 7,
                  'STDEV.P': 8,
                  'SUM': 9,
                  'VAR.S': 10,
                  'VAR.P': 11,
                  'MEDIAN': 12,
                  'MODE.SNGL': 13,
                  'LARGE': 14,
                  'SMALL': 15,
                  'PERCENTILE.INC': 16,
                  'QUARTILE.INC': 17,
                  'PERCENTILE.EXC': 18,
                  'QUARTILE.EXC': 19}

TABLE_STYLE_MAP: dict[tuple[str, str, str], str] = {
    ("light", "black", "simple"):   "TableStyleLight1",
    ("light", "blue", "simple"):   "TableStyleLight2",
    ("light", "red", "simple"):   "TableStyleLight3",
    ("light", "green", "simple"):   "TableStyleLight4",
    ("light", "purple", "simple"):   "TableStyleLight5",
    ("light", "teal", "simple"):   "TableStyleLight6",
    ("light", "orange", "simple"):   "TableStyleLight7",
    ("light", "black", "outline"):   "TableStyleLight8",
    ("light", "blue", "outline"):   "TableStyleLight9",
    ("light", "red", "outline"):   "TableStyleLight10",
    ("light", "green", "outline"):   "TableStyleLight11",
    ("light", "purple", "outline"):   "TableStyleLight12",
    ("light", "teal", "outline"):   "TableStyleLight13",
    ("light", "orange", "outline"):   "TableStyleLight14",
    ("light", "black", "clean"):   "TableStyleLight15",
    ("light", "blue", "clean"):   "TableStyleLight16",
    ("light", "red", "clean"):   "TableStyleLight17",
    ("light", "green", "clean"):   "TableStyleLight18",
    ("light", "purple", "clean"):   "TableStyleLight19",
    ("light", "teal", "clean"):   "TableStyleLight20",
    ("light", "orange", "clean"):   "TableStyleLight21",

    ("medium", "black", "simple"):   "TableStyleMedium1",
    ("medium", "blue", "simple"):   "TableStyleMedium2",
    ("medium", "red", "simple"):   "TableStyleMedium3",
    ("medium", "green", "simple"):   "TableStyleMedium4",
    ("medium", "purple", "simple"):   "TableStyleMedium5",
    ("medium", "teal", "simple"):   "TableStyleMedium6",
    ("medium", "orange", "simple"):   "TableStyleMedium7",
    ("medium", "black", "outline"):   "TableStyleMedium8",
    ("medium", "blue", "outline"):   "TableStyleMedium9",
    ("medium", "red", "outline"):   "TableStyleMedium10",
    ("medium", "green", "outline"):   "TableStyleMedium11",
    ("medium", "purple", "outline"):   "TableStyleMedium12",
    ("medium", "teal", "outline"):   "TableStyleMedium13",
    ("medium", "orange", "outline"):   "TableStyleMedium14",
    ("medium", "black", "clean"):   "TableStyleMedium15",
    ("medium", "blue", "clean"):   "TableStyleMedium16",
    ("medium", "red", "clean"):   "TableStyleMedium17",
    ("medium", "green", "clean"):   "TableStyleMedium18",
    ("medium", "purple", "clean"):   "TableStyleMedium19",
    ("medium", "teal", "clean"):   "TableStyleMedium20",
    ("medium", "orange", "clean"):   "TableStyleMedium21",

    ("dark", "black", "simple"):   "TableStyleDark1",
    ("dark", "blue", "simple"):   "TableStyleDark2",
    ("dark", "red", "simple"):   "TableStyleDark3",
    ("dark", "green", "simple"):   "TableStyleDark4",
    ("dark", "purple", "simple"):   "TableStyleDark5",
    ("dark", "teal", "simple"):   "TableStyleDark6",
    ("dark", "orange", "simple"):   "TableStyleDark7",
    ("dark", "black", "clean"):   "TableStyleDark8",
    ("dark", "blue", "clean"):   "TableStyleDark9",
    ("dark", "green", "clean"):   "TableStyleDark10",
    ("dark", "teal", "clean"):   "TableStyleDark11",
}


def makehash():
    return collections.defaultdict(makehash)


@dataclass
class FormatRule:
    format: str
    condition: str | None = None  # use "_column_" as a placeholder for the column reference

    def __post_init__(self):
        if not self.format.strip():
            raise ValueError("format cannot be empty")

@dataclass
class OperationRule:
    agg_functions: str | list[str]      # one agg function per column — parallel to `columns`
    columns: str | list[str]            # the columns being aggregated together
    operators: Operation | list[Operation] | None = None  # joins the terms: n columns -> n-1 operators

    def __post_init__(self):
        # normalize to lists first
        if isinstance(self.agg_functions, str):
            self.agg_functions = [self.agg_functions]
        if isinstance(self.columns, str):
            self.columns = [self.columns]
        if isinstance(self.operators, str):
            self.operators = [self.operators]
        elif self.operators is None:
            self.operators = []

        if not self.agg_functions:
            raise ValueError("agg_functions cannot be empty")
        if not self.columns:
            raise ValueError("columns cannot be empty")


class Table:

    def __init__(self,
             name: str,
             data: pd.DataFrame,
             title: str | None = None,
             start_col: int = 1,
             title_row: int | None = 1,
             header_row: int = 2,
             data_row: int = 3,
             total_row: Literal['bottom', 'top'] = 'bottom',
             freeze_panes: int | tuple | None = None,
             title_align: Literal['center', 'left', 'right'] = 'center',
             header_comments: dict[str, str] | None = None,
             style: tuple[TableTier, TableColor, TableVariant] = ('medium', 'blue', 'simple')):

        # validate data input
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"data must be a pandas DataFrame, got {type(data).__name__}")
        if data.empty:
            raise ValueError("data cannot be empty")

        # validate table name
        if not name or not name.strip():
            raise ValueError("name cannot be empty")

        # validate positive row and column values
        if start_col < 1:
            raise ValueError(f"start_col must be >= 1, got {start_col!r}")
        if title_row < 1 or header_row < 1 or data_row < 1:
            raise ValueError("row values must be >= 1")

        # validate correct sequence of title, header and data rows
        if title_row == header_row or title_row == data_row or header_row == data_row:
            raise ValueError('row initializers cannot be the same value')
        if title and (title_row > header_row or title_row > data_row):
            raise ValueError('title row must come before header and data')
        if header_row > data_row:
            raise ValueError('header row must come before data')

        # validate Literals
        if total_row not in ('bottom', 'top'):
            raise ValueError(f"total_row must be 'bottom' or 'top', got {total_row!r}")
        if title_align not in ('center', 'left', 'right'):
            raise ValueError(f"title_align must be 'center', 'left', or 'right', got {title_align!r}")

        # validate freeze_panes structure
        if isinstance(freeze_panes, tuple) and len(freeze_panes) != 2:
            raise ValueError(f"freeze_panes tuple must have exactly 2 elements, got {freeze_panes!r}")

        # ensure header_comments references valid columns
        header_comments = header_comments if header_comments is not None else {}
        if header_comments:
            unknown = set(header_comments) - set(data.columns)
            if unknown:
                raise ValueError(f"header_comments references unknown columns: {unknown}")

        # validate tier/color combination
        tier, color, variant = style

        if style not in TABLE_STYLE_MAP:
            available_variants = [v for (t, c, v) in TABLE_STYLE_MAP if t == tier and c == color]
            if available_variants:
                raise ValueError(
                    f"No style for tier={tier!r} color={color!r} variant={variant!r}. "
                    f"Valid variants for tier={tier!r} color={color!r}: {available_variants}"
                )
            else:
                available_colors = sorted({c for (t, c, v) in TABLE_STYLE_MAP if t == tier})
                raise ValueError(
                    f"No style for tier={tier!r} color={color!r}. "
                    f"Valid colors for tier={tier!r}: {available_colors}"
                )

        # set parameters
        self.name = name
        self.data = data
        self.title = title
        self.start_col = start_col
        self.title_row = title_row
        self.header_row = header_row
        self.data_row = data_row
        self.total_row = total_row
        self.freeze_panes = freeze_panes
        self.title_align = title_align
        self.header_comments = header_comments
        self.style = TABLE_STYLE_MAP[style]

        # set properties
        self.__column_formats = {}
        self.__total_formats = {}
        self.__header_formats = {}
        self.__total_operations = {} # empty means no total row (no operations)


    def __add_formats(self, format_dict: dict, columns: str | list[str], rules: FormatRule | list[FormatRule]):
        """standard wrapper for adding formats to aspects of a table by column and condition

        Args:
            format_dict (dict): the dictionary to store the format by aspect of the table
            columns (str | list[str]): the column(s) to apply the rule to
            rules (FormatRule | list[FormatRule]): the rule (format and condition) to apply to the column(s)
        """
        # normalize both inputs to lists so the rest of the method only deals with one shape
        if isinstance(columns, str):
            columns = [columns]
        if isinstance(rules, FormatRule):
            rules = [rules]

        # loop through the list of columns
        for column in columns:
            # loop through the list of rules
            for rule in rules:
                # replace placeholder for multiple columns
                condition = rule.condition.replace("_column_", column) if rule.condition else None

                # store the format and condition to be applied to the column
                if column not in format_dict:
                    format_dict[column] = [(rule.format, condition)]
                else:
                    format_dict[column].append((rule.format, condition))


    def add_column_formats(self, columns: str | list[str], rules: FormatRule | list[FormatRule]):
        """defines a column format / conditional formatting rule

        Args:
            columns (str | list[str]): the column(s) to apply the rule to
            rules (FormatRule | list[FormatRule]): the rule (format and condition) to apply to the column(s)
        """
        self.__add_formats(self.__column_formats, columns, rules)


    def add_total_formats(self, columns: str | list[str], rules: FormatRule | list[FormatRule]):
        """defines a total format / conditional formatting rule
        
        Args:
            columns (str | list[str]): the column(s) to apply the rule to
            rules (FormatRule | list[FormatRule]): the rule (format and condition) to apply to the column(s)
        """
        self.__add_formats(self.__total_formats, columns, rules)


    def add_header_formats(self, columns: str | list[str], rules: FormatRule | list[FormatRule]):
        """defines a header format / conditional formatting rule
        
        Args:
            columns (str | list[str]): the column(s) to apply the rule to
            rules (FormatRule | list[FormatRule]): the rule (format and condition) to apply to the column(s)
        """
        self.__add_formats(self.__header_formats, columns, rules)


    def add_total_operation(self, columns: str | list[str], rule: OperationRule):
        """defines how total operations / aggregates should be calculated

        Args:
            columns (str | list[str]): the column(s) to put the total
            rule (OperationRule): the rule for defining the total /agg operation
        """
        # normalize
        if isinstance(columns, str):
            columns = [columns]

        terms = [
            f'_xlfn.AGGREGATE({AGG_CONVERSION[agg.upper()]}, 5, {self.name}[{column}])'
            for agg, column in zip(rule.agg_functions, rule.columns)
        ]

        formula = terms[0]
        for operator, term in zip(rule.operators, terms[1:]):
            formula += f' {operator} {term}'

        formula = f'=({formula})'

        for column in columns:
            self.__total_operations[column] = formula


    def hide_columns(self):
        ...


    def get_column_formats(self):
        return self.__column_formats


    def get_total_formats(self):
        return self.__total_formats


    def get_header_formats(self):
        return self.__header_formats


    def get_total_operations(self):
        return self.__total_operations