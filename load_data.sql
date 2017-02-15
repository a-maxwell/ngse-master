/*
 after ma set-up yung db:

 guys pakipalitan yung path below. yung '/home...'
 questions.csv and categories.csv are found inside the csvs folder.
 then run
 \i '<path to this file>'
*/

COPY questions FROM '/home/daisyreeviscaya/Desktop/NGSE/csvs/questions.csv' with delimiter as ',' csv;
COPY categories FROM '/home/daisyreeviscaya/Desktop/NGSE/csvs/categories.csv' with delimiter as ',' csv;
