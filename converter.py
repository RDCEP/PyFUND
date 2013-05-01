import re
import glob
import os
import warnings

class Parameters(object): pass
class Behaviors(object): pass

class Variable(object):
  def __init__(self, *vargs): pass 

class IVariable1Dimensional(Variable): pass
class IVariable2Dimensional(Variable): pass
class IParameter1Dimensional(Variable): pass
class IParameter2Dimensional(Variable): pass

def convert_file(filename):
  new_name = "components/{0}.py".format(os.path.basename(filename)[:-3])
  
  source = open(filename).read()
  destination = open(new_name, 'w')
  result = [ ]
  
  def _class(match):
    found_any = [ True ]
    
    def _interface(match):
      result.append("class {0}(Parameters):".format(match.group(1)))
      
      index = match.group(0)[1:].find('interface')
      
      if index < 0:
        index = len(match.group(0))
      
      next_description = None
      
      def _ivariable(match):
        if match.group(1):
          desc = re.sub(r'(^//?/?)|(</?summary>)', '', match.group(1)).strip()
        else:
          desc = None # '[[{0}]]'.format(match.group(4))
        
        result.append("   {3} = {1}({2!r}, {0!r})".format(desc, match.group(3), [ x.strip() for x in match.group(4).split(',') ], match.group(5)))
        
        # print match.groups()[1:] # print "{0} {1}".format(match.group(1), match.group(2))
        return ""
      
      found_any[0] = True
      
      chunk = match.group(0)[:index]
      
      re.sub(r'(//([^\r\n]*?)[ \t\r\n]+?)?(I[a-zA-Z0-9]+)<([^>]*?)> ([a-zA-Z0-9]+) {.*?}', _ivariable, chunk, flags = re.DOTALL)
      
      result.append("")
      return match.group(0)[index:]
    
    left = match.group(2)
    while found_any[0]:
      found_any[0] = False
      left = re.sub(r'interface ([A-Za-z0-9]+).*?{(.*)}.*?', _interface, left, flags = re.DOTALL)
    
    found_any = [ True ]
    
    def _run(match):
      index = match.group(0)[1:].find('public class')
      
      if index < 0:
        index = len(match.group(0))
      
      code = left[match.start(2) : min(match.end(2), match.start(0) + index) ]
      
      code = re.sub(r'[ \t\r\n]*{[ \t]*[\r\n]', ':\n', code)
      code = re.sub(r'}', '', code)
      code = re.sub(r'var ', '', code)
      code = re.sub(r'//.+', '', code)
      code = re.sub(r'/\*.*?\*/', '', code)
      code = re.sub(r'if ([^\r\n:]+)([\r\n])', r'if \1:\2', code)
      
      def _lambda(match):
        args = [ x.split(' ')[1].strip() for x in match.group(2).split(',') ]
        return "def {0}({1}):\n{2}".format(match.group(1), ', '.join(args), match.group(3))
          
      code = re.sub(r'([A-Za-z0-9]+)\s*=\s*Funcifier.Funcify\s*\(\s*\((.*?)\).*?:(.*?)[\r\n][ \t]*\)', _lambda, code, flags = re.DOTALL)
      code = re.sub(r'(\s+)=\s+([^;]+?);', r'\1= (\2);', code)
      code = re.sub(r'foreach \((.+?) in (.+?)\):', r'for \1 in \2:', code)
      code = re.sub(r'else\s*([\r\n])', r'else:\1', code)
      code = re.sub(r'Math\.[A-Za-z]+', lambda x: x.group(0).lower(), code)
      code = re.sub(r'throw\s+new', 'raise', code)
      code = re.sub(r'(\s+)(.+?):\s*[\r\n \t]*[\r\n]\1([^ \t\r\n])', r'\1\2:\n\1  pass\n\1\3', code)
      code = re.sub(r'[\r\n](\s+)(Double|double|float|int) ', r'\1', code)
      code = re.sub(r'GetValues<Region>', 'GetValuesOfRegion', code)
      code = re.sub(r';[ \t]*(\r\n|\n)', '\n', code)
      code = re.sub(r'\s+\?\s+', ' and ', code)
      code = re.sub(r'\s+:\s+', ' or ', code)
      code = re.sub(r'else if', 'elif', code)
      code = re.sub(r'&&', 'and', code)
      code = re.sub(r'\|\|', 'or', code)
      code = re.sub(r'!', 'not ', code)
      code = re.sub(r'\(([^=(]+)=>(.+?)\)', r'(lambda \1:\2)', code)
      
      state_class = match.group(1)
      
      if state_class.endswith('Component'):
        state_class = state_class[:-len('Component')]
      
      result.append("class {0}(Behaviors):".format(match.group(1)))
      result.append("   state_class = I{0}State".format(state_class))
      result.append("   ")
      result.append("   def run(state, clock):")
      result.append(code)
      
      found_any[0] = True
      
      return match.group(0)[index:]
    
    left = match.group(2)
    
    while found_any[0]:
      found_any[0] = False
      left = re.sub(r'public class ([A-Za-z0-9]+).*?{.*?public void Run.*?{(.*)}.*?}', _run, left, flags = re.DOTALL)
    
    return ""
  
  re.sub(r'namespace Fund\.Components\.([A-Za-z0-9]*).*?{(.*)}', _class, source, flags = re.DOTALL)
  
  generated_code = "\n".join(result)
  
  # print generated_code
  
  autopep8 = None
  
  try:
    import autopep8
  except ImportError:
    warnings.warn("You do not have autopep8 installed; the generated "
                  "code is going to be terribly mangled.")
  
  exec generated_code in globals()
  
  if autopep8:
    generated_code = autopep8.fix_string(generated_code)
    exec generated_code in globals()
  
  destination.write(generated_code)
  destination.close()

for file in glob.glob('../fund-master/FundComponents/*.cs'):
  convert_file(file)