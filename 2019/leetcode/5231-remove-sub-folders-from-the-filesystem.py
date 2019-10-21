class Solution:
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        tree = {}
        
        for f in folder:
            path = f.split('/')
            if len(path) < 2: continue

            path = path[1:]
            root = tree
            should_end = True
            for p in path:
                if '#' in root:
                    should_end = False
                    break
                if p not in root: root[p] = {}
                root = root[p]
            if should_end: root['#'] = {}
                
        return self.get_ret(tree, '')
        
    def get_ret(self, tree:dict, base:str):
        ret = []

        if '#' in tree:
            return [base]
        
        for node in tree:
            path = base + '/' + node
            ret += self.get_ret(tree[node], path)
            
        return ret