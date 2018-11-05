from bs import Option
import csv

 
def exists(name):
    if(name =='-'):
        return False
    else:
        return True

def greek_calc():

    #===========================================================================
    # TO CHECK OPTION CALCULATIONS
    #===========================================================================
    s = 56.37  # spot
    k = 60  # strike
    exp_date = '20171215'
    eval_date = '20140528'
    rf = 0.01  # rate of interest
    vol = 0.2074  # IV
    div = 0.014  # dividend
    right = 'C'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right,
                 div = div)
    price, delta, theta, gamma = opt.get_all()
    print("-------------- FIRST OPTION -------------------")
    print("Price CALL: " + str(price))  # 2.97869320042
    print("Delta CALL: " + str(delta))  # 0.664877358932
    print("Theta CALL: " + str(theta))  # 0.000645545628288
    print("Gamma CALL:" + str(gamma))   # 0.021127937082

def read_csv_call():
    filename = 'nse_options_chain.csv'

    with open(filename,'r') as fd:
        reader = csv.reader(fd)
        headers = next(reader, None)
        for row in reader:
            call_iv = row[3]
            call_ltp = row[4]
            strike = row[10]
            put_iv = row[17]
            put_ltp = row[16]

            

            if(exists(call_iv) and exists(call_ltp) and exists(strike) and exists(put_iv) and exists(put_ltp)):
                # print(call_iv,call_ltp,strike,put_iv,put_ltp)
                s = float(25732)
                k = float(strike)
                eval_date = '20181105'
                exp_date = '20181106'
                rf = 0.07
                vol = float(call_iv)/100
                right = 'C'
                div = 0

                opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right,div = div)

                # print (s,k,eval_date,exp_date,rf,vol,right,div)
                price, delta, theta, gamma = opt.get_all()
                # print("-------------- FIRST OPTION -------------------")
                # print("Price CALL: " + str(price))  # 2.97869320042
                # print("Delta CALL: " + str(delta))  # 0.664877358932
                # print("Theta CALL: " + str(theta))  # 0.000645545628288
                # print("Gamma CALL:" + str(gamma))   # 0.021127937082
                # print ("strike: ",k,"act: ",call_ltp,"calculated: ",price,"delta: ", delta, "theta: ",theta, "gamma: ",gamma)
                print ("strike: ",strike,"delta: ", delta, "theta: ",theta, "gamma: ",gamma)


def read_csv_put():
    filename = 'nse_options_chain.csv'

    with open(filename,'r') as fd:
        reader = csv.reader(fd)
        headers = next(reader, None)
        for row in reader:
            call_iv = row[3]
            call_ltp = row[4]
            strike = row[10]
            put_iv = row[17]
            put_ltp = row[16]

            

            if(exists(call_iv) and exists(call_ltp) and exists(strike) and exists(put_iv) and exists(put_ltp)):
                # print(call_iv,call_ltp,strike,put_iv,put_ltp)
                s = float(25732)
                k = float(strike)
                eval_date = '20181105'
                exp_date = '20181106'
                rf = 0.07
                vol = float(put_iv)/100
                right = 'P'
                div = 0

                opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right,div = div)

                # print (s,k,eval_date,exp_date,rf,vol,right,div)
                price, delta, theta, gamma = opt.get_all()
                # print("-------------- FIRST OPTION -------------------")
                # print("Price CALL: " + str(price))  # 2.97869320042
                # print("Delta CALL: " + str(delta))  # 0.664877358932
                # print("Theta CALL: " + str(theta))  # 0.000645545628288
                # print("Gamma CALL:" + str(gamma))   # 0.021127937082
                # print ("strike: ",k,"act: ",call_ltp,"calculated: ",price,"delta: ", delta, "theta: ",theta, "gamma: ",gamma)
                print ("strike: ",strike,"delta: ", delta, "theta: ",theta, "gamma: ",gamma)

if __name__ == '__main__':
    # greek_calc()
    read_csv_call()
    print('-'*100)
    read_csv_put()


