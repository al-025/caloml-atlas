import uproot as ur

class cell_info:
    '''
    Convenience accessor for retrieving cell information via the 'cluster_cell_ID' hash.
    The constructor takes a path to a root file containing the 'CellGeo' tree as its only argument.
    Given the 'cluster_cell_ID' hash for a cell, retrieve its information by indexing a cell_info object with that hash; for example:
      ci = cell_info('inputfile.root')
      ci[1149470720] # hash for a cell in TileBar0 (cell_geo_sampling=12)
    Alternatively, you can use the member functions 'get_cell_info' or 'get_cell_info_vector' directly by passing them the hash as their only argument.
    '''
    meta_tree = 'CellGeo'
    id_branch = 'cell_geo_ID'
    
    def __init__(self, metafile):
        with ur.open(metafile) as ifile:
            self.meta_keys = ifile[self.meta_tree].keys()
            self.celldata = ifile[self.meta_tree].arrays(
                self.meta_keys)
            
        self.id_map = {}
        for i, cell_id in enumerate(self.celldata[self.id_branch][0]):
            self.id_map[cell_id] = i

    def get_cell_info(self, cell_id):
        return {
            k : self.celldata[k][0][self.id_map[cell_id]]
            for k in self.meta_keys
        }
    
    def get_cell_info_vector(self, cell_id):
        res = []
        for k in self.meta_keys:
            if(k == self.id_branch):
                continue
            res.append(self.celldata[k][0][self.id_map[cell_id]])
        return res
    
    def __getitem__(self, key):
        return self.get_cell_info(key)

