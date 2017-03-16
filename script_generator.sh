#!/bin/bash

echo "COPY categories(category_id, category, form_type_id) FROM '"$(pwd)"/csvs/categories.csv' with delimiter as ',' csv;" > load_data.sql
echo "COPY questions(question_id, question, form_type_id, category_id) FROM '"$(pwd)"/csvs/questions.csv' with delimiter as ',' csv;" >> load_data.sql