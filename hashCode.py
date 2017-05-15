import cProfile
import pstats
import os
# 性能分析装饰器定义
def do_cprofile(filename):
    """
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            # Flag for do profiling or not.
            DO_PROF = True
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper

filename = ".\mkm_run.prof"
class Solution:
    """
    @param key: A String you should hash
    @param HASH_SIZE: An integer
    @return an integer
    """
    @do_cprofile(filename)
    def hashCode(self, key, HASH_SIZE):
        # write your code here
        length = len(key)
        pows = 1
        sum = 0
        while length > 0:
            length -= 1
            sum += ord(key[length]) * pows
            pows *= 33
        return sum % HASH_SIZE

print(Solution().hashCode('ubuntufsdfgsdfsdfsdafsdsdfsdfsdfdsfsdfsdfsdfsdfsdfsdfsfsdfsdfwstfrhsrtjhryujtyjktyhtfgewrtgyhrtyertghfghgfgruisdyhtghtgherityeritgeryigfidfghiugiyaertighaeuifgastgeryterytuieryguihgusdhgukdhgksdfhfh', 1007))
print(pstats.Stats(filename).strip_dirs().sort_stats('cumtime').print_stats(10, 2.0, '.*'))