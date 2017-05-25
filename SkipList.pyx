from libc.limits cimport INT_MAX, INT_MIN

cdef class _node:
	cdef public int key
	forward = []

	def __init__(self, int key):
		self.key = key

cdef class skipList:
	cdef double p
	cdef public _node HEADER, NIL
	cdef int maxLevel

	def __init__(self, double p, int maxLevel):
		self.p = p
		self.maxLevel = maxLevel
		self.HEADER = _node(INT_MIN)
		self.NIL = _node(INT_MAX)
		cdef int i
		for i in range(maxLevel):
			self.HEADER.forward.append(self.NIL)