class Solution:
    """
    @param key: A String you should hash
    @param HASH_SIZE: An integer
    @return an integer
    """
    def hashCode(self, key, HASH_SIZE):
        # write your code here
        length = len(key)
        pows = 1
        sum = 0
        while length > 0:
            length -= 1
            sum += ord(key[length]) * pows % HASH_SIZE
            pows = pows * 33 % HASH_SIZE
        return sum % HASH_SIZE