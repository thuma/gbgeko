<html>
<head>
<title>GBG Eko</title>
<style>
tr.data td:last-child {
  text-align: right;
}
</style>
</head>
<body>
<form method='get'>
  <table>
  <tr>
  <td>Summera per:</td>
  %   for col in headervalues:
      <td><input name="groupby" value="{{ col }}" type="checkbox" {{ "checked" if (col in selected) else "" }}>{{ col }}</td>
  %   end
  </tr>
  <tr>
  <td>Visa:</td>
  % for col in headervalues:
  <td><select name="filter">
      <option value="">Alla</option>
  %   for value in headervalues[col]:
      <option value="{{ col }}-{{ value[0] }}" {{ "selected" if col in filters and filters[col] == value[0] else "" }}>{{ value[0] }}</option>
  %   end
  </select></td>
  % end
  </tr>
  </table>
<input type='submit' value="Visa"></form>
<table>
  <tr>
  %   for col in headers:
      <th>{{ col }}</th>
  %   end
  </tr>
  % for item in rows:
  <tr class="data">
  %   for col in item:
      <td>{{ col }}</td>
  %   end
  </tr>
  % end
</table>
</body>
</html>
