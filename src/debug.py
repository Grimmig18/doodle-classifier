import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

from src.data_loader import DataLoader as DL

dl = DL()
data = dl.load_data_from_file(dl.PIZZA)
