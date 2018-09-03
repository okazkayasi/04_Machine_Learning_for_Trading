import numpy as np

def test_run():
    a = np.array([(20,25,10,23,26,32,10,5,0),(0,2,50,20,0,1,28,5,0)])
    print a

    # calculate mean
    mean = a.mean()
    print mean

    # masking
    print a[a<mean]

    # change using masking
    a[a<mean] = mean
    print a

    a = np.array([(1,2,3,4,5),(10,20,30,40,50)])
    print "\n original array: \n", a

    # multiply
    print "\n Multiply: \n",2*a

    # divide 
    print "\nDivide: \n", a/2.0

    b = np.array([(100,200,300,400,500),(1,2,3,4,5)])
    
    # add two arrays
    print "\nAdd a + b: \n", a+b

    # multiply two array - this will do elemenet-wise
    print "\nElement-wise multiplication: \n", a*b
    

if __name__ =="__main__":
    test_run()