import pandas as pd

def get_labels_beginner():
    l_ = pd.read_csv('test_labels/test_labels1.csv')
    return l_['bank_account']
    
def get_labels_advanced():
    l_ = pd.read_csv('test_labels/client_test_labels.csv')
    return l_['target']

