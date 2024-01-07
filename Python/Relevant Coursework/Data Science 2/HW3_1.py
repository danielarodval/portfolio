file_name = input('Enter a file name: ')
try:
    with open(file_name) as file:
        data = file.readlines()
        total = 0
        if data[0] == 'account_id,total_debt,contact_email\n':
            pass
        else:
            print('Invalid file format!')
        del data[0]
        for i in data:
            try:
                int(i.split(',')[0])
            except ValueError:
                print("Non int found in first column!")
            try:
                float(i.split(',')[1])
            except ValueError:
                print("Non float found in second column!")
            total = total + float(i.split(',')[1])
        print(total)
        file.close()
except:
    print('No file found!')
del data, file, file_name, i, total 