# exposure_parsers
Set of parsers to process dwellings based on census data.
A mapping scheme is needed considering two or three variables

## input_data
Make sure the data is stored in an excel file (.xlsx) with at least:
* A sheet with census data for a given administrative level
* A sheet with the mapping scheme
NOTE: The maping scheme must perfectly match the variables used in the census.
Check the exmaple data given in "example-data.xlsx"

The user can parse information based on two or three variables: 
var1: in the rows (e.g. floor material)
var2: in the first column (e.g. wall material)
var3: in the second column (e.g. type of dwelling)