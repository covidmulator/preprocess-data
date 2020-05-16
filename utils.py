def min_max_normalize(lst):
  normalized = []

  for value in lst:
    normalized_num = (value - min(lst)) / (max(lst) - min(lst))
    normalized.append(normalized_num)
  
  return normalized

not_exist = [
  'CITY / BUS',
  'LACKAWANNA',
  'NEWARK BM BW',
  'NEWARK C',
  'NEWARK HM HE',
  'PAVONIA/NEWPORT',
  'NEWARK HW BMEBE'
]

url_generator = lambda x: f'http://web.mta.info/developers/data/nyct/turnstile/turnstile_{x}.txt'

fields = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS']
