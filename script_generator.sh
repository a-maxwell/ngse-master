#!/bin/bash

echo "COPY questions FROM '"$(pwd)"/questions.csv' with delimiter as ',' csv;" > load_data.sql
echo "COPY categories FROM '"$(pwd)"/categories.csv' with delimiter as ',' csv;" >> load_data.sql