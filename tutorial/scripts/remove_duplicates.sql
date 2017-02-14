DELETE FROM items
WHERE id IN (SELECT id
              FROM (SELECT id,
                             ROW_NUMBER() OVER (partition BY price, location, start_time, end_time ORDER BY id) AS rnum
                     FROM items) t
              WHERE t.rnum > 1);