import paramiko
def check(hostname,username,password,port=22):
        client=paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, username=username, password=password, port=port)
        stdin,stdout,strerror=client.exec_command('cat /etc/login.defs | grep "^PASS"')
        output = stdout.readlines()
        rules = {
                "PASS_MAX_DAYS":("max", 90),
                "PASS_MIN_DAYS":("min", 1),
                "PASS_MIN_LEN":("min", 8),
                "PASS_WARN_AGE":("min", 7)
        }

        for line in output:
                parts=line.split()
                name, value=parts[0], int(parts[1])
                if name in rules:
                        check_type, threshold=rules[name]
                check_rules = (check_type=="max" and value>threshold) or (check_type=="min" and value<threshold)
                if check_rules:
                        print(name,value,"不合格" )
                else:
                        print(name,value,"合格")
        client.close()


check("your IP", " your username", "your password")