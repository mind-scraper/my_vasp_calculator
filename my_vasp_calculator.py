from ase.calculators.calculator import Calculator
import tempfile
from ase.io import read
import os

class VASP(Calculator):
    implemented_properties = ['energy', 'forces']
    
    def __init__(self, command=None, **kwargs):        
        self.command = command
        Calculator.__init__(self, **kwargs)
    
    def calculate(self, atoms=None, properties=['energy'], system_changes=['positions']):
        Calculator.calculate(self, atoms, properties, system_changes)

        workdir = tempfile.mkdtemp(
            prefix="vasp_",
            dir=os.getcwd()
        )

        old_dir = os.getcwd()
        os.chdir(workdir)
        os.system("cp ../INCAR .")
        os.system("cp ../POTCAR .")
        os.system("cp ../KPOINTS .")
        
        atoms.write('POSCAR')

        # Run VASP
        os.system(self.command)

        # Read results
        atoms = read('OUTCAR')
        
        # Combine results
        self.results['energy'] = atoms.get_potential_energy()
        self.results['forces'] = atoms.get_forces()

        os.chdir(old_dir)
        os.system(f"rm -r {workdir}")
