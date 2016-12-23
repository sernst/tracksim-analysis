# BEB 500 Catalog Export

This notebook is an exporter that converts the Cadence database data for the 
BEB 500 tracksite into a CSV file that is structured to match the A16 field 
measurements catalog format.

Not all columns in the catalog are accounted for because they are not 
applicable to Cadence source data. The following columns are populated with
empty values by this notebook:

{% for column in csv_columns -%}
{%- if column.fill is not none -%}
* {{ column.name }}
{% endif -%}
{%- endfor %}

The remaining columns:

{% for column in csv_columns -%}
{%- if column.fill is none -%}
* {{ column.name }}
{% endif -%}
{%- endfor %}

are populated with values from the Cadence database throughout
this notebook.
