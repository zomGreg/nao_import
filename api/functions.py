def flatten_json(data):
  result = []
  for i in data:
    result.append([i[0],i[1]])
  return result
