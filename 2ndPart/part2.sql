-- SECOND PART OF TEST CASE - TO CREATE SQL QUERY

SELECT
  apl.date,
  apl.call_result,
  SUM(apl.audio_duration) as duration_sum,
  COUNT(apl.call_result) as quantity,
  p.name as proj_name,
  s.name as serv_name
FROM ((audio_parameters_list as apl
  INNER JOIN project as p ON apl.project_id = p.id)
  INNER JOIN server as s  ON apl.server_id = s.id)
  GROUP BY apl.call_result, apl.date, p.name, s.name
  ORDER BY quantity DESC, duration_sum DESC;
