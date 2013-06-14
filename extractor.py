# 
# This script extracts parameter sets from the .xlsm files 
# in the fund/ directory and stores them as YAML. In this
# way we can more easily read them to generate interfaces
# and validation.

import glob
import xlrd
import string
import re
import fund

class NormalDistribution(object):
  def __init__(self, *values):
    if len(values) == 1:
      match = re.match(r'NormalDistribution\(([^;]+); ([^;]+).+\)', values[0])
      self.mean, self.stddev = map(float, match.groups())
    else:
      self.mean, self.stddev = values
  
  def __repr__(self):
    return u'NormalDistribution({0}, {1})'.format(self.mean, self.stddev)

def _extract_as_typed(object):
  if type(object) in (str, unicode):
    if object.startswith('Normal'):
      return NormalDistribution(object)
  return object

class Table(object):
  def __init__(self, sheet, rows, columns):
    all_cells = [ ]
    
    for row in rows:
      row_data = [ ]
      for column in columns:
        row_data.append(_extract_as_typed(sheet.cell(rowx = row, colx = column).value))
      all_cells.append(row_data)
    self.all_cells = all_cells
    
    self.sheet_name = sheet.name
    self.height = len(rows)
    self.width = len(columns)
  
  @classmethod
  def detect_single(self, sheet, row, start_column):
    extent = start_column
    for column in xrange(start_column, sheet.ncols):
      if not sheet.cell(row, column).value:
        break
      else:
        extent = column
    return Table(sheet, [ row ], range(start_column, extent + 1))
  
  @classmethod
  def detect_several(self, sheet, start_row, start_column):
    extent_column = start_column
    extent_row = start_row
    
    for column in xrange(start_column, sheet.ncols):
      if not sheet.cell(start_row, column).value:
        pass
      else:
        extent_column = column
    
    for row in xrange(start_row, sheet.nrows):
      for column in xrange(start_column, sheet.ncols):
        if sheet.cell(row, column).value:
          break
      else:
        break
      extent_row = row
    
    return Table(sheet, range(start_row, extent_row + 1),
                        range(start_column, extent_column + 1))
  
  def extract_field(self, field_name):
    top_columns = self.all_cells[0]
    left_columns = [ x[0] for x in self.all_cells ]
    
    if field_name in top_columns: # we are a column
      index = top_columns.index(field_name)
      values = [ x[index] for x in self.all_cells ]
      headers = [ x[0] for x in self.all_cells ]
      return zip(headers, values)
    
    elif field_name in [ x[0] for x in self.all_cells ]: # we are a row
      index = left_columns.index(field_name)
      values = self.all_cells[index]
      headers = self.all_cells[0]
      return zip(headers, values)
    
    elif field_name == self.sheet_name:
      results = [ ]
      
      for column_index, column in enumerate(top_columns):
        if column_index == 0:
          continue
        for row_index, row in enumerate(left_columns):
          if row_index == 0:
            continue
          
          results.append((column, row, self.all_cells[row_index][column_index]))
      
      return results
    else:
      return None
  
  def describe(self):
    for row in self.all_cells:
      print(repr(row))
    print('')

def main():
  workbook = xlrd.open_workbook('fund/Fund/Data/Parameter - Base.xlsm')
  
  all_tables = [ ]
  count_warnings = 0
  
  for sheet_name in workbook.sheet_names():
    sheet = workbook.sheet_by_name(sheet_name)
    row = 0
    
    while row < sheet.nrows:
      cell = sheet.cell(colx = 0, rowx = row)
      second = sheet.cell(colx = 1, rowx = row) if sheet.ncols > 1 else None
      
      if cell.value in ('Region', 'Name', 'Year') or ((not cell.value) and second.value):
        table = Table.detect_several(sheet, row, 0)
        row += table.height
        
        if table.height == 1:
          print('Warning: there is bizarre data on sheet "{0}" starting at cell A{1}:'.
              format(sheet_name, row))
          table.describe()
          print('---')
          print('')
          count_warnings += 1
        
        all_tables.append(table)
        
      elif cell.ctype == 1 and (' ' in cell.value or len(cell.value) > 20):
        row += 1 # comment
      elif cell.value in ('', None):
        row += 1 # blank cell
      else:
        table = Table.detect_single(sheet, row, 0)
        row += table.height
        all_tables.append(table)
  
  print '{0} table(s) extracted, {1} warnings'.format(len(all_tables), count_warnings)
  
  for table in all_tables:
    table.extract_field('ypcgrowth')

if __name__ == '__main__':
  main()