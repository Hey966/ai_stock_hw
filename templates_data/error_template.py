ERROR_TEMPLATE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>錯誤</title>
  {{ base_style|safe }}
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>{{ title }}</h1>
      <div class="value">{{ msg }}</div>
    </div>
  </div>
</body>
</html>
"""