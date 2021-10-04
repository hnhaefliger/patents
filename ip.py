from patents import *

i = 0
a = b = 0
diff = []

while True:
    cases = new_york.get_cases(i)

    for case in cases:
        try:
            plaintiff =  search.get_matching_records(case[0])
            defendant = search.get_matching_records(case[1])

            if plaintiff and defendant:
                print(plaintiff)
                print(defendant)
                print('match')

                with open('suits.txt', 'a+') as f:
                    f.write(plaintiff[0]['year'] + defendant[0]['year'] + '\n')

                a += 1

                if plaintiff[0]['year'] < defendant[0]['year']:
                    b += 1

                diff.append(int(plaintiff[0]['year']) - int(defendant[0]['year']))

                print(b / a, sum(diff)/len(diff))
                print('')

        except:
            pass

    i += 1