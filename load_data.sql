COPY categories(category_id, category, form_type_id) FROM '/Users/Peioris/Projects/cs192/csvs/categories.csv' with delimiter as ',' csv;
COPY questions(question_id, question, form_type_id, category_id) FROM '/Users/Peioris/Projects/cs192/csvs/questions.csv' with delimiter as ',' csv;
