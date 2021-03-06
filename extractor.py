# 
# This script extracts parameter sets from the .xlsm files 
# in the fund/ directory and stores them as YAML. In this
# way we can more easily read them to generate interfaces
# and validation.

import glob
import sys
import string
import re
import os
import csv

try:
  import xlrd
except ImportError:
  print("Please install the xlrd library. You might find it useful to run")
  print("  pip install -r requirements.txt")
  print("or to use virtualenv to do this.")
  sys.exit(1)

if not os.path.isdir('fund'):
  print('Unable to find the FUND model. Please download it and place it in ./fund,')
  print('in the root directory of the PyFUND project.')
  sys.exit(1)

from fund import FUND, NormalDistribution

def _extract_as_typed(object):
  """
  Typifies this object as a value of the given
  type.
  """
  if type(object) in (str, unicode):
    object = object.strip()
    if object.startswith('Normal'):
      return NormalDistribution(object)
    elif '2000y' in object:
      return int(object[:-1])
  if type(object) in (float,):
     if int(object) == object:
        return int(object)
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
    self.prefix = ""
  
  @classmethod
  def detect_single(self, sheet, row, start_column):
    """
    Searches for a 1D (horizontal) table at this offset.
    """
    extent = start_column
    for column in xrange(start_column, sheet.ncols):
      if not sheet.cell(row, column).value:
        break
      else:
        extent = column
    return Table(sheet, [ row ], range(start_column, extent + 1))
  
  @classmethod
  def detect_several(self, sheet, start_row, start_column):
    """
    Searches for a 2D table at this offset.
    """
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
    """
    Extracts all values of a given parameter as a list of ordered
    pairs.
    """
    top_columns = self.all_cells[0]
    left_columns = [ x[0] for x in self.all_cells ]
    
    if not field_name.startswith(self.prefix):
      return None
    else:
      field_name = field_name[len(self.prefix):]
    
    tci = [ str(x).lower().strip() for x in top_columns ]
    lci = [ str(x).lower().strip() for x in left_columns ]
    fn = field_name.lower()
    
    if self.height == 1 and tci[0] == fn:
      if (' ' in str(top_columns[1]) and
          'Distribution' not in str(top_columns[1])):
         return None
      return [[ field_name ], [ str(top_columns[1]) ]]
    
    elif self.width == 1 and tci[0] == fn:
      return [[ field_name ], [ str(self.all_cells[1][0]) ]]
    
    elif fn in tci: # we are a column
      index = tci.index(fn)
      values = [ x[index] for x in self.all_cells ]
      headers = [ x[0] for x in self.all_cells ]
      return zip(headers, values)
    
    elif fn in lci: # we are a row
      index = lci.index(fn)
      values = self.all_cells[index]
      headers = self.all_cells[0]
      return zip(headers, values)
    
    elif fn == self.sheet_name.lower():
      results = [ ]
      already_hit = set()
      
      machine_readable_name = "{0}_2".format(field_name) # FIXME!
      results.append(FUND.all_options[machine_readable_name].index_by + [field_name])
      
      for column_index, column in enumerate(top_columns):
        if column_index == 0:
          continue
        for row_index, row in enumerate(left_columns):
          if row_index == 0:
            continue
          
          value = self.all_cells[row_index][column_index]
          
          results.append((column, row, value))
          already_hit.add((column, row))
          
          if (row, column) not in already_hit:
            results.append((row, column, value)) # FIXME
          
           # Tables are not drawn in any particular orientation,
           # so we duplicate them in the dictionary with the hope
           # that at least one way of doing it will work. That
           # policy doesn't work with REG -> REG spreadsheets, so
           # in that case we make a wild guess.
      
      return results
    else:
      return None
  
  def describe(self):
    for row in self.all_cells:
      print(repr(row))
    print('')

def process_sheet(sheet, prefix = ""):
   """
   Processes the given xlrd sheet, returning a generator of all tables in that
   sheet.
   """
   
   row = 0
   
   while row < sheet.nrows:
     cell = sheet.cell(colx = 0, rowx = row)
     second = sheet.cell(colx = 1, rowx = row) if sheet.ncols > 1 else None
     
     if cell.value in ('Region', 'Name', 'Year') or ((not cell.value) and second.value):
       table = Table.detect_several(sheet, row, 0)
       table.prefix = prefix
       
       row += table.height
       
       yield table
       
     elif cell.ctype == 1 and (' ' in cell.value or len(cell.value) > 20):
       row += 1 # comment
     elif cell.value in ('', None):
       row += 1 # blank cell
     else:
       table = Table.detect_single(sheet, row, 0)
       table.prefix = prefix
       
       row += table.height
       yield table

def main():
  workbook = xlrd.open_workbook('fund/Fund/Data/Parameter - Base.xlsm')
  scenario = xlrd.open_workbook('fund/Fund/Data/Parameter - SRES A1b.xlsm')
  
  all_tables = [ ]
  
  # Process first workbook.
  for sheet_name in workbook.sheet_names():
    sheet = workbook.sheet_by_name(sheet_name)
    
    all_tables.extend(process_sheet(sheet))
  
  # Process scenario.
  for sheet_name in workbook.sheet_names():
    sheet = workbook.sheet_by_name(sheet_name)
    
    all_tables.extend(process_sheet(sheet, prefix = 'scen'))
  
  print('{0} table(s) extracted'.format(len(all_tables)))
  
  options_specified = 0
  options_total = 0
  
  for old_parameter_file in glob.glob('parameters/*.csv'):
    os.unlink(old_parameter_file)
  
  for option in FUND.all_options:
    unmangled_name, arity = option.rsplit('_', 1)
    for table in all_tables:
      value = table.extract_field(unmangled_name)
      if value:
        with open('parameters/{0}.csv'.format(unmangled_name), 'w') as fp:
          writer = csv.writer(fp)
          for row in value:
            writer.writerow(row)
        options_specified += 1
        break
    options_total += 1
  
  print('{0} option(s) specified of {1} total; {2} omitted'.
    format(options_specified, options_total, options_total - options_specified))

if __name__ == '__main__':
  main()