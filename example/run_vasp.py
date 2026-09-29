from ase.io import read
from copy import copy
from my_vasp_calculator import VASP

# Read atoms
atoms = read('structure.xyz')

# Set calculator
calc = VASP(command='mpirun -np 8 vasp_std > vasp.log')

atoms.calc = copy(calc)

# etc.
