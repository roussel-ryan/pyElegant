import logging
import operator

import numpy as np

""" a simple reverse-polish notation calculator
    shouldn't be too hard to extend this--variables seem like a natural progression
"""

def error_string(token, values):
    plural = ''
    if values > 1:
        plural = 's'

    return 'Error: %s takes %d value%s.' % (token, values, plural)


operators = {
    '+': [operator.add, 2],
    '-': [operator.sub, 2],
    '*': [operator.mul, 2],
    '/': [operator.truediv, 2],
    '^': [operator.pow, 2],
    '%': [operator.mod, 2],
    '_': [lambda x: -x, 1],
    'acos': [lambda x: np.arccos(x),1],
    'dsin': [lambda x: np.sin(np.deg2rad(x)),1],
}

def rpn(expression):
    stack = []
    #logging.debug(expression)
	
	
    for token in expression.split():
        #logging.debug(stack)
        if token in operators:
            try:
                if operators[token][1] == 1:
                    stack.append(operators[token][0](stack.pop()))
                elif operators[token][1] == 2:
                    stack.append(operators[token][0](stack.pop(-2), stack.pop()))
            except:
                logging.error(error_string(token, operators[token][1]))
        else:
            try:
                stack.append(float(token))
            except ValueError:
                return expression
                #logging.warning('Error: only real numbers or %s.' % ''.join(operators.keys()))
    if len(stack) == 1:
        return stack.pop()
    else:
        logging.error('Error: badly formed.')
        return None
	
		
		
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    exp = '0.29 20 dsin / 20 * 180 / -1 acos *'
    logging.debug(rpnCalc(exp))
	
