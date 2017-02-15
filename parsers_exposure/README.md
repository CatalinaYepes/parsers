# exposure_parsers
Set of parsers to process dwellings based on census data.
A mapping scheme is needed considering one, two or three variables

## input_data
Make sure the data is stored in an excel file (.xlsx) with at least:
* A sheet with census data for a given administrative level
* A sheet with the mapping scheme.

NOTE: The mapping scheme must perfectly match the census variables.
Check the example data given in "example-data.xlsx"

The user can parse information based on one, two or three variables: 
var1: in the rows (e.g. floor material)
var2: in the first column (e.g. wall material)
var3: in the second column (e.g. type of dwelling)