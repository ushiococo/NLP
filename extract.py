path3 = "C:\\Users\\Qiaoyan\\Downloads\\test1\\client_hostname2.txt"


with open(path3, 'r') as f3:
    x1 = f3.readlines()

    a = [x1[i:i+6000] for i in range(0,len(x1),6000)]
    print(a)
    count = 0
    for i in a:
        count += 1
        with open(f'C:\\Users\\Qiaoyan\\Downloads\\test1 - Copy\\test2\\test{count}.txt','w') as f:

        # with open(f'test{count}.txt','w') as f:
           i = ''.join(i)
           i = i.replace("\t", " ")
        #    i = i.replace("\n", " ")
        #    print(type(i))
           f.writelines(str(i) +"\n")
        print("Extracting done!")