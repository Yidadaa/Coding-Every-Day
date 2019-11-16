class Solution:
    def generateSentences(self, synonyms: List[List[str]], text: str) -> List[str]:
        union = {}
        
        for pair in synonyms:
            for p in pair:
                if p not in union:
                    union[p] = p
                    
        def find(x):
            if union[x] == x: return x
            union[x] = find(union[x])
            return union[x]
        
        def set_u(x, y):
            y = find(y)
            while union[x] != x:
                _x = union[x]
                union[x] = y
                x = _x
            union[x] = y
                
        for pair in synonyms:
            s, t = pair
            set_u(s, t)
            
        group = {}
        
        for p in union:
            k, v = find(union[p]), p
            if k not in group: group[k] = []
            group[k].append(v)

        for k in group:
            group[k] = sorted(group[k])
            
        text = text.split(' ')
        ret = ['']
        
        for c in text:
            to_concat = [c] if c not in union else group[find(c)]
            new_ret = []
            for s in ret:
                for re_c in to_concat:
                    new_ret.append(s + (' ' if len(s) else '') + re_c)
                ret = new_ret
                    
        return ret
