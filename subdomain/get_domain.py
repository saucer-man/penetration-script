from tld import get_tld

with open("domain.txt",'w') as f1:
    with open("urls_0619.txt","r") as f2:
        for domain in f2.readlines():
            if domain.strip() =="":
                continue
            try:
                a = get_tld(domain.strip(),as_object=True, fix_protocol=True)
                f1.write(a.fld)
                f1.write("\n")
            except:
                print(domain.strip())

