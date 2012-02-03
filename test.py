import nose
import ast
from symbolic import Symbol

def test_add():
	expr = "x + 1"
	
def test_sub():
	expr = "x - 1"

def test_mul():
	expr = "x * 1"

def test_div():
	expr = "x / 1"

def test_idiv():
	expr = "x + 1"

def test_iter():
	expr = "iter(x)"

def test_getattribute():
	expr = "x.foo"

def test_invert():
	expr = "~x"

def test_index():
	pass

def test_neg():
	expr = "-x"

def test_pos():
	expr = "+x"

def test_call():
	expr = "x()"

def test_getitem():
	expr1 = "x[y]"
	expr2 = "x[0:-1]"

def test_floordiv():
	expr = "x // 1"

def test_mod():
	expr = "x % 1"

def test_divmod():
	pass

def test_pow():
	expr = "x ** 1"

def test_lshift():
	expr = "x << 1"

def test_rshift():
	expr = "x >> 1"

def test_div():
	expr = "x / 1"

def test_contains():
	expr = "x in 1"

def test_eq():
	expr = "x == 1"

def test_ne():
	expr = "x != 1"

def test_le():
	expr = "x <= 1"

def test_lt():
	expr = "x < 1"

def test_gt():
	expr = "x > 1"

def test_ge():
	expr = "x >= 1"

def test_cmp():
	expr = "cmp(x, 1)"

def test_and():
	expr = "x & 1"

def test_xor():
	expr = "x ^ 1"

def test_or():
	expr = "x | 1"

def test_iand():
	expr = "x &= 1"

def test_ixor():
	expr = "x ^= 1"

def test_ior():
	expr = "x |= 1"

def test_iadd():
	expr = "x += 1"

def test_isub():
	expr = "x -= 1"

def test_imul():
	expr = "x *= 1"

def test_idiv():
	expr = "x /= 1"

def test_itruediv():
	expr = "x /= 1"

def test_ifloordiv():
	expr = "x //= 1"

def test_imod():
	expr = "x %= 1"

def test_ipow():
	expr = "x **= 1"

def test_ilshift():
	expr = "x <<= 1"

def test_irshift():
	expr = "x >>= 1"

if __name__ == "__main__":
	nose.runmodule()