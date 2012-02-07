import nose
import ast
from symbolic import Symbol, compile_sym

def test_add():
	x = 4
	symbol = 4
	sym = Symbol() + 2
	expr = "x + 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4 + 2
	assert x == symbol

def test_sub():
	x = 4
	symbol = 4
	sym = Symbol() - 2
	expr = "x - 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4 - 2
	assert x == symbol

def test_mul():
	x = 4
	symbol = 4
	sym = Symbol() * 2
	expr = "x * 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4 * 2
	assert x == symbol

def test_div():
	x = 4
	symbol = 4
	sym = Symbol() / 2
	expr = "x / 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4 / 2
	assert x == symbol

def test_iter():
	x = iter(Symbol())
	expr = "iter(x)"
	p_expr = ast.parse(expr)

def test_getattribute():
	x = Symbol().foo
	expr = "x.foo"
	p_expr = ast.parse(expr)

def test_invert():
	x = 1
	symbol = 1
	sym = ~Symbol()
	expr = "~x"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == -2
	assert x == symbol

def test_index():
	pass

def test_neg():
	x = 1
	symbol = 1
	sym = -Symbol()
	expr = "-x"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == -1
	assert x == symbol

def test_pos():
	x = 1
	symbol = 1
	sym = +Symbol()
	expr = "+x"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 1
	assert x == symbol

def test_call():
	x = 4
	symbol = 4
	three = []
	four = {}
	sym = Symbol()(1, two=2, *three, **four)
	expr = "x(1, two=2, *three, **four)"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	print ast.dump(p_expr)
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert x == symbol

def test_getitem():
	x = [1, 2, 3, 4, 5]
	symbol = [1, 2, 3, 4, 5]
	sym1 = Symbol()[0]
	sym2 = Symbol()[1:-1]
	expr1 = "x[0]"
	expr2 = "x[1:-1]"
	p_expr1 = ast.parse(expr1, mode='eval')
	p_expr2 = ast.parse(expr2, mode='eval')
	c_expr1 = compile(ast.fix_missing_locations(p_expr1), '', 'eval')
	c_expr2 = compile(ast.fix_missing_locations(p_expr2), '', 'eval')
	c_sym1 = compile_sym(sym1)
	c_sym2 = compile_sym(sym2)
	x = eval(c_expr1)
	symbol = eval(c_sym1)
	assert symbol == 1
	assert x == symbol
	x = [1, 2, 3, 4, 5]
	symbol = [1, 2, 3, 4, 5]
	x = eval(c_expr2)
	symbol = eval(c_sym2)
	assert symbol == [2, 3, 4]
	assert x == symbol

def test_floordiv():
	x = 3
	symbol = 3
	sym = Symbol() // 2
	expr = "x // 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 3 // 2
	assert x == symbol

def test_mod():
	x = 4
	symbol = 4
	sym = Symbol() % 2
	expr = "x % 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4 % 2
	assert x == symbol

def test_divmod():
	pass

def test_pow():
	x = 2
	symbol = 2
	sym = Symbol() ** 2
	expr = "x ** 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 4
	assert x == symbol

def test_rshift():
	x = 1
	symbol = 1
	sym = Symbol() >> 1
	expr = "x >> 1"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 1 >> 1
	assert x == symbol

def test_lshift():
	x = 1
	symbol = 1
	sym = Symbol() << 1
	expr = "x << 1"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == 1 << 1
	assert x == symbol

def test_contains():
	x = 1 in Symbol()
	expr = "x in 1"
	p_expr = ast.parse(expr)

def test_cmp():
	x = Symbol() >= 1
	expr = "x >= 1"
	p_expr = ast.parse(expr)

def test_eq():
	x = 1
	symbol = 1
	sym = Symbol() == 1
	expr = "x == 1"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_ne():
	x = 1
	symbol = 1
	sym = Symbol() != 2
	expr = "x != 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_le():
	x = 1
	symbol = 1
	sym = Symbol() <= 1
	expr = "x <= 1"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_lt():
	x = 1
	symbol = 1
	sym = Symbol() < 2
	expr = "x < 2"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_gt():
	x = 1
	symbol = 1
	sym = Symbol() > 0
	expr = "x > 0"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol


def test_ge():
	x = 1
	symbol = 1
	sym = Symbol() >= 1
	expr = "x >= 1"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_and():
	x = True
	symbol = True
	sym = Symbol() & False
	expr = "x & False"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert x == symbol
	assert symbol == False


def test_xor():
	x = True
	symbol = True
	sym = Symbol() ^ True
	expr = "x ^ True"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == False
	assert x == symbol

def test_or():
	x = False
	symbol = False
	sym = Symbol() | True
	expr = "x | True"
	p_expr = ast.parse(expr, mode='eval')
	c_expr = compile(ast.fix_missing_locations(p_expr), '', 'eval')
	c_sym = compile_sym(sym)
	x = eval(c_expr)
	symbol = eval(c_sym)
	assert symbol == True
	assert x == symbol

def test_iand():
	x = Symbol()
	x &= 1
	expr = "x &= 1"
	p_expr = ast.parse(expr)

def test_ixor():
	x = Symbol()
	x ^= 1
	expr = "x ^= 1"
	p_expr = ast.parse(expr)

def test_ior():
	x = Symbol()
	x |= 1
	expr = "x |= 1"
	p_expr = ast.parse(expr)

def test_iadd():
	x = Symbol()
	x += 1
	expr = "x += 1"
	p_expr = ast.parse(expr)

def test_isub():
	x = Symbol()
	x -= 1
	expr = "x -= 1"
	p_expr = ast.parse(expr)

def test_imul():
	x = Symbol()
	x *= 1
	expr = "x *= 1"
	p_expr = ast.parse(expr)

def test_idiv():
	x = Symbol()
	x /= 1
	expr = "x /= 1"
	p_expr = ast.parse(expr)

def test_itruediv():
	x = Symbol()
	x /= 1
	expr = "x /= 1"
	p_expr = ast.parse(expr)

def test_ifloordiv():
	x = Symbol()
	x //= 1
	expr = "x //= 1"
	p_expr = ast.parse(expr)

def test_imod():
	x = Symbol()
	x %= 1
	expr = "x %= 1"
	p_expr = ast.parse(expr)

def test_ipow():
	x = Symbol()
	x **= 1
	expr = "x **= 1"
	p_expr = ast.parse(expr)

def test_ilshift():
	x = Symbol()
	x <<= 1
	expr = "x <<= 1"
	p_expr = ast.parse(expr)

def test_irshift():
	x = Symbol()
	x >>= 1
	expr = "x >>= 1"
	p_expr = ast.parse(expr)

if __name__ == "__main__":
	nose.runmodule(argv=["-d", "-s"])
