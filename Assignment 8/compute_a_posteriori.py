# Posterior Probability Task 1
import sys

def main(argv):
    p = [[0 for x in range(100)] for y in range(100)] 
    q = [[0 for x in range(100)] for y in range(100)] 

    # prior probabilities
    p[0][1] = 0.1
    p[0][2] = 0.2
    p[0][3] = 0.4
    p[0][4] = 0.2
    p[0][5] = 0.1
    # 6 - for Cherry 7- for Lime
    p[0][6] = 0.5
    p[0][7] = 0.5
    # cherry in bag 
    q[0][1] = 1
    q[0][2] = 0.75
    q[0][3] = 0.5
    q[0][4] = 0.25
    q[0][5] = 0
    # Lime in bag   
    q[1][1] = 0
    q[1][2] = 0.25
    q[1][3] = 0.50
    q[1][4] = 0.75
    q[1][5] = 1
    
    # if no observation case
    if len(argv) != 2:
       filenm = open('result.txt', 'w')
       filenm.write('Observation sequence Q: \r\n')
       filenm.write('Length of sequence: 0 \r\n\n')
       filenm.write('After Observation  1 : \r\n\n')
       filenm.write('p(h1 | Q) = %8.5f \r\n'%(p[0][1]))
       filenm.write('p(h2 | Q) = %8.5f \r\n'%(p[0][2]))
       filenm.write('p(h3 | Q) = %8.5f \r\n'%(p[0][3]))
       filenm.write('p(h4 | Q) = %8.5f \r\n'%(p[0][4]))
       filenm.write('p(h5 | Q) = %8.5f \r\n'%(p[0][5]))
       filenm.write('Probability that the next candy we pick will be C, given no observation : %8.5f \r\n'%(p[0][6]))
       filenm.write('Probability that the next candy we pick will be L, given no observation : %8.5f \r\n'%(p[0][7]))
       filenm.close()
       sys.exit(0)
 
    observation_length = len(argv[1])
    # oaaabservation_str = []
    observation_str = list(argv[1])
    j = 1
    filenm = open('result.txt', 'w')
    filenm.write('Observation sequence Q: %s\r\n'%(argv[1]))
    filenm.write('Length of sequence: %d\r\n\n'%(len(argv[1])))
    temp = ''

    # calculating the probabilities
    for k in range(observation_length):
        temp = temp + observation_str[k]; 
        # print '\nObs '+ str(k) + ' = ' + temp 
        filenm.write('After Observation  %d : %s \r\n\n'%(k + 1, temp))
        for l in range(5):
            i = l + 1
            if observation_str[k] == 'C':
               p[j][i] = (q[0][i] * p[j - 1][i]) / p[0][6]
               filenm.write('p(h%s | Q) = %8.5f\r\n'%(i,p[j][i]))
            else:
                if observation_str[k] == 'L':
                   p[j][i] = (q[1][i] * p[j - 1][i]) / p[0][7]
                   filenm.write('p(h%s | Q) = %8.5f\r\n'%(i,p[j][i]))               
        p[j][6] = 0
        # for t + 1 observations
        for h in range(5):
            i = h + 1
            p[j][6] = p[j][6] + q[0][i] * p[j][i]
            p[0][6] = p[j][6]; 
            p[j][7] = p[j][7] + q[1][i] * p[j][i]
            p[0][7] = p[j][7]
        filenm.write('Probability that the next candy we pick will be C, given %s : %8.5f \r\n'%(observation_str[k], p[0][6]))
                    
        filenm.write('Probability that the next candy we pick will be L, given %s : %8.5f \r\n\n'%(observation_str[k], p[0][7]))
           
        j = j + 1
    filenm.close()
    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)