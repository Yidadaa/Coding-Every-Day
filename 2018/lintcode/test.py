import random

def gen_data(N=10):
    '''
    生成N组测试数据
    '''
    ISSUE_SUM = 10 # 每个人最多可能有ISSUE_SUM个issue
    base_name_code = ord('A')
    users = []
    issue_num = 0
    for i in range(N):
        name = chr(base_name_code + i)
        issue_count = random.randint(1, ISSUE_SUM)
        issues = []
        for j in range(issue_count):
            issue_num += 1
            issues.append({ 'issue_name': name + '#' + str(issue_num), 'size': random.random() * 2 })
        users.append({
            'username': name,
            'issuses': issues
        })

    return users

if __name__ == '__main__':
    data = gen_data()
    print(data)