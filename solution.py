from fractions import Fraction

def solution(m):
    #normalizes the rows of the matrix
    normalized = [[Fraction(0,1) for y in range(len(m))] for x in range (len(m))]
    for i in range(len(m)):
        sum = 0
        for j in range(len(m[i])):
            sum += m[i][j]
        if sum == 0:
            sum = 1
        for j in range(len(m[i])):
            normalized[i][j] = Fraction(m[i][j],sum)
    #print(normalized)

    #retrieve the non-terminal rows
    nonterminalRows = []
    for i in range(len(normalized)):
        allZero = True
        for j in range(len(normalized[i])):
            if normalized[i][j] != 0:
                allZero = False
                break
        if normalized[i][i] != 1 and allZero == False: #not terminal
            nonterminalRows.append(i)
    #print(nonterminalRows)
    
    size = len(nonterminalRows)

    #solve for q, the bottom right quadrant
    q = []
    for i in range(size):
        q.append([])
    count = 0
    for i in nonterminalRows:
        for j in nonterminalRows:
            q[count].append(normalized[i][j])
        count += 1 
    #print(q)

    #solve for s, the bottom left quadrant
    s = []
    for i in range(size):
        s.append([])
    count = 0
    for i in nonterminalRows:
        for j in range(len(m)):
            if j not in nonterminalRows:
                s[count].append(normalized[i][j])
        count += 1
    #print(s)

    #create the identity matrix
    identity = [[0 for y in range(size)] for x in range(size)]
    for i in range(size):
        identity[i][i] = 1
    #print(identity)
    
    #solution is A = S + QA, or A = (I-Q)^-1 * S
    ans = multiply(invert(subtract(identity,q)),s)[0]
    #print(ans)
    ans.append(1)

    #clean out the fractions
    max = 0
    toCheck = []
    while checkFrac(ans) == False:
        for i in range(len(ans)):
            if ans[i].denominator > max:
                max = ans[i].denominator
        for i in range(len(ans)):
            ans[i] *= max
            toCheck.append(max)
    for i in range(len(ans)):
        ans[i] = ans[i].numerator

    primes = prime(ans[len(ans)-1]).reverse() 
    count = 0
    while primes:
        passed = True
        for j in range(len(ans)):
            if ans[j] % primes[0] != 0:
                passed = False
                break
        if passed:
            for j in range(len(ans)):
                ans[0] /= primes[0]
        primes.pop()
    return ans

def prime(a):
    i = 2
    primes = []
    while i*i <= a:
        if a % i == 1:
             i += 1
        else: 
            a /= i
            a = int(a)
            primes.append(i)
    if a > 1:
        primes.append(a)
    return primes

def checkFrac(a):
    for i in range(len(a)-1):
        if a[i].denominator != 1:
            return False #there's still a fraction
    return True #all integers

def subtract(a,b): #a-b
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] -= b[i][j]
    return a

def multiply(a,b): #a*b
    result = [[0 for y in range(len(b[0]))] for x in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                result[i][j] += a[i][k] * b[k][j]
    return result
        
def invert(a):
    size = len(a)
    identity = [[0 for y in range(size)] for x in range(size)]
    for i in range(size):
        identity[i][i] = 1
    for currentDiag in range(0,size):
        currentMultiplier = 1 / a[currentDiag][currentDiag]
        for j in range(size): #adjust current row so the diagonal is 1
            a[currentDiag][j] *= currentMultiplier
            identity[currentDiag][j] *= currentMultiplier
        for i in range(size): #set all the other rows to 0
            if i == currentDiag: 
                continue
            currentMultiplier = a[i][currentDiag]
            for j in range(size): #adjust corresponding values
                a[i][j] -= currentMultiplier * a[currentDiag][j]
                identity[i][j] -= currentMultiplier * identity[currentDiag][j]
    return identity

"""
print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))

print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))

print(solution(
    [[0, 1, 0, 0, 0, 1], 
    [0, 0, 0, 0, 0, 0], 
    [4, 0, 0, 3, 2, 0],  
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]]))

#print(solution([[0,1],[0,0]]))

print(prime(60))

print(subtract([[1,0,0],[0,1,0],[0,0,1]],[[1,2,3],[4,5,6],[7,8,9]]))

print(invert([[1,3,3],[1,4,3],[1,3,4]]))

print(multiply([[-3,-2],[3,4],[-1,6],[0,5]],[[7,8,9],[-3,3,1]]))

print(multiply([[-1,1,5],[-2,3,0],[2,4,6]],[[7,8,-4],[-3,9,1],[-1,2,4]]))

print(invert([[1,2,3],[0,1,4],[5,6,0]]))

print(invert([[1,0],[0,1]]))
"""
