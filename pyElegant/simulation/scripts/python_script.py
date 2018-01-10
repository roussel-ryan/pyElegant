from pyElegant import utils
import sys
import sdds
import numpy as np
import importlib.util

def runTransformation(main):
	input_filename = sys.argv[2]
	input_params,input_param_def,input_columns,input_col_def = utils.read_sdds_file(input_filename,include_definitions=True)
	output_file = sdds.SDDS(1)
	data = np.asarray([item for name, item in input_columns.items()]).T
	result = main(data)
	paged_result = [[col.tolist()] for col in result]
	for name,item in input_params.items():
		output_file.parameterName.append(name)
		output_file.parameterDefinition.append(input_param_def[name])
		output_file.parameterData.append([item])
	for name,item in zip(input_columns.keys(),paged_result):
		output_file.columnName.append(name)
		output_file.columnDefinition.append(input_col_def[name])
		output_file.columnData.append(item)
	assert input_filename[-len('.in'):] == '.in'
	output_file.save(input_filename[:-len('.in')] + '.out')

def main():
    script_path = sys.argv[1]
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    runTransformation(foo.main)

if __name__ == '__main__':
    main()
