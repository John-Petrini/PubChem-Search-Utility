import tkinter as tk
from PIL import ImageTk
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import MolToImage
import sys

class PubChemSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PubChem Search Utility")
        
        # Create and place the input field
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=10)

        # Create and place the "Enter" button
        self.enter_button = tk.Button(master, text="Report", command=self.display_info)
        self.enter_button.pack(pady=5)

        # Create and place the output window
        self.output_window = tk.Text(master, height=15, width=50, state=tk.DISABLED, font=('Time New Roman', 10))
        self.output_window.pack(pady=10)

        #generating default molecular image
        image_update = None
        self.mol_structure = tk.Label(master)
        self.mol_structure.pack(pady=5)
            
    # function to obtain , report information from pubchem
    def display_info(self):
        pubchem_id = self.entry.get()
        if pubchem_id:
            # configuration of output winfow
            self.output_window.config(state=tk.NORMAL)
            self.output_window.delete(1.0, tk.END)
            
            # generation of outputs
            info_string, c_smiles = self.molecule_search(pubchem_id)
            self.print_output(info_string)
            self.draw_structure(c_smiles)
            
        else:
            print("Please enter a PubChem ID before searching.")
    
    #functiion to find and report number of matching ID's
    def molecule_search(self, pubchem_id):
        compounds = pcp.get_compounds(pubchem_id, 'name')
        
        if compounds:
            c_len = len(compounds)
            
            if c_len == 1:
                self.print_output(f'One entry found for: {pubchem_id}')
                info_string, c_smiles = self.compound_info(pubchem_id, compounds)
                return info_string, c_smiles
                       
            elif c_len > 1:
                self.print_output(f'{c_len} entries found for: {pubchem_id}. This implies {c_len} stereoisomers exist.')
                info_string, c_smiles = self.compound_info(pubchem_id, compounds)
                return info_string, c_smiles
                
        else:
            self.print_output(f'No entry found for: {pubchem_id}')

            
    # function returns info & smiles for compounds
    def compound_info(self, pubchem_id, compounds):
        info_string = ""
        mol_count = 1
        for compound in compounds:
            info_string += f"Result No. {mol_count} for {pubchem_id} \n"
            c_id = compound.cid
            c_formula = compound.molecular_formula
            c_smiles = compound.canonical_smiles
            c_mol_wt = compound.molecular_weight
            c_exact_mass = compound.exact_mass
            c_logp = compound.xlogp
            
            info_string += f"PubChem CID: {c_id}\n"
            info_string += f"Molecular Formula: {c_formula}\n"
            info_string += f"Canonical Smiles: {c_smiles}\n"
            info_string += f"Molecular Weight: {c_mol_wt}\n"
            info_string += f"Exact Mass: {c_exact_mass}\n"
            info_string += f"LogP: {c_logp}\n\n"
            mol_count += 1
            
        return info_string, c_smiles
    
    
    # function to print
    def print_output(self, text):
        self.output_window.config(state=tk.NORMAL)
        self.output_window.delete(1.0, tk.END)
        
        # Redirect print statements to the output window
        sys.stdout = OutputRedirector(self.output_window)
        
        # Display the output, disable editing
        print(text)
        self.output_window.config(state=tk.DISABLED)
    
    
    # function to draw structure
    def draw_structure(self, c_smiles):
        # extracting rdchem object
        kekule = Chem.MolFromSmiles(c_smiles)
        if kekule:
            # convert RDKit molecule to PIL image
            pil_image = MolToImage(kekule)
            
            # convert PIL to compatible format
            image_update = ImageTk.PhotoImage(pil_image)
            
            # updating widget
            self.mol_structure.config(image=image_update)
            self.mol_structure.image = image_update

            # fore immediate update of widget
            self.mol_structure.update_idletasks()

# class to redirect print statements to Tk output window
class OutputRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)

# initializeing program
def main():
    root = tk.Tk()
    app = PubChemSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
