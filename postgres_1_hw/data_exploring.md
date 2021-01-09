```python
import pandas as pd
```


```python
df = pd.read_csv('P9-ConsumerComplaints.csv', low_memory=False)
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date Received</th>
      <th>Product Name</th>
      <th>Sub Product</th>
      <th>Issue</th>
      <th>Sub Issue</th>
      <th>Consumer Complaint Narrative</th>
      <th>Company Public Response</th>
      <th>Company</th>
      <th>State Name</th>
      <th>Zip Code</th>
      <th>Tags</th>
      <th>Consumer Consent Provided</th>
      <th>Submitted via</th>
      <th>Date Sent to Company</th>
      <th>Company Response to Consumer</th>
      <th>Timely Response</th>
      <th>Consumer Disputed</th>
      <th>Complaint ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2013-07-29</td>
      <td>Consumer Loan</td>
      <td>Vehicle loan</td>
      <td>Managing the loan or lease</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Wells Fargo &amp; Company</td>
      <td>VA</td>
      <td>24540</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Phone</td>
      <td>2013-07-30</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>468882</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2013-07-29</td>
      <td>Bank account or service</td>
      <td>Checking account</td>
      <td>Using a debit or ATM card</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Wells Fargo &amp; Company</td>
      <td>CA</td>
      <td>95992</td>
      <td>Older American</td>
      <td>NaN</td>
      <td>Web</td>
      <td>2013-07-31</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>468889</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2013-07-29</td>
      <td>Bank account or service</td>
      <td>Checking account</td>
      <td>Account opening, closing, or management</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Santander Bank US</td>
      <td>NY</td>
      <td>10065</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Fax</td>
      <td>2013-07-31</td>
      <td>Closed</td>
      <td>Yes</td>
      <td>No</td>
      <td>468879</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2013-07-29</td>
      <td>Bank account or service</td>
      <td>Checking account</td>
      <td>Deposits and withdrawals</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Wells Fargo &amp; Company</td>
      <td>GA</td>
      <td>30084</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Web</td>
      <td>2013-07-30</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>468949</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2013-07-29</td>
      <td>Mortgage</td>
      <td>Conventional fixed mortgage</td>
      <td>Loan servicing, payments, escrow account</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Franklin Credit Management</td>
      <td>CT</td>
      <td>6106</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Web</td>
      <td>2013-07-30</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>475823</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>65494</th>
      <td>2015-05-26</td>
      <td>Mortgage</td>
      <td>Other mortgage</td>
      <td>Loan servicing, payments, escrow account</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Nationstar Mortgage</td>
      <td>TX</td>
      <td>75401</td>
      <td>Servicemember</td>
      <td>NaN</td>
      <td>Referral</td>
      <td>2015-05-29</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>1393114</td>
    </tr>
    <tr>
      <th>65495</th>
      <td>2015-05-06</td>
      <td>Mortgage</td>
      <td>Other mortgage</td>
      <td>Loan modification,collection,foreclosure</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Bank of America</td>
      <td>CA</td>
      <td>92880</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Referral</td>
      <td>2015-05-07</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>1364367</td>
    </tr>
    <tr>
      <th>65496</th>
      <td>2015-05-20</td>
      <td>Debt collection</td>
      <td>I do not know</td>
      <td>Cont'd attempts collect debt not owed</td>
      <td>Debt resulted from identity theft</td>
      <td>My identity was stolen back in XXXX 2008 when ...</td>
      <td>Company chooses not to provide a public response</td>
      <td>Performant Financial Corporation</td>
      <td>FL</td>
      <td>322XX</td>
      <td>NaN</td>
      <td>Consent provided</td>
      <td>Web</td>
      <td>2015-05-20</td>
      <td>Closed with non-monetary relief</td>
      <td>Yes</td>
      <td>No</td>
      <td>1385089</td>
    </tr>
    <tr>
      <th>65497</th>
      <td>2015-05-06</td>
      <td>Debt collection</td>
      <td>Other (i.e. phone, health club, etc.)</td>
      <td>Cont'd attempts collect debt not owed</td>
      <td>Debt is not mine</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Afni, Inc.</td>
      <td>CA</td>
      <td>92065</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Phone</td>
      <td>2015-05-07</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>1363039</td>
    </tr>
    <tr>
      <th>65498</th>
      <td>2015-04-27</td>
      <td>Mortgage</td>
      <td>Conventional fixed mortgage</td>
      <td>Application, originator, mortgage broker</td>
      <td>NaN</td>
      <td>Previous lender ( XXXX ) offered mortgage rate...</td>
      <td>Company believes the complaint is the result o...</td>
      <td>USAA Savings</td>
      <td>OR</td>
      <td>972XX</td>
      <td>NaN</td>
      <td>Consent provided</td>
      <td>Web</td>
      <td>2015-04-27</td>
      <td>Closed with explanation</td>
      <td>Yes</td>
      <td>No</td>
      <td>1348370</td>
    </tr>
  </tbody>
</table>
<p>65499 rows × 18 columns</p>
</div>




```python
df.iloc[0]

```




    Date Received                                   2013-07-29
    Product Name                                 Consumer Loan
    Sub Product                                   Vehicle loan
    Issue                           Managing the loan or lease
    Sub Issue                                              NaN
    Consumer Complaint Narrative                           NaN
    Company Public Response                                NaN
    Company                              Wells Fargo & Company
    State Name                                              VA
    Zip Code                                             24540
    Tags                                                   NaN
    Consumer Consent Provided                              NaN
    Submitted via                                        Phone
    Date Sent to Company                            2013-07-30
    Company Response to Consumer       Closed with explanation
    Timely Response                                        Yes
    Consumer Disputed                                       No
    Complaint ID                                        468882
    Name: 0, dtype: object




```python
df.dtypes
```




    Date Received                   object
    Product Name                    object
    Sub Product                     object
    Issue                           object
    Sub Issue                       object
    Consumer Complaint Narrative    object
    Company Public Response         object
    Company                         object
    State Name                      object
    Zip Code                        object
    Tags                            object
    Consumer Consent Provided       object
    Submitted via                   object
    Date Sent to Company            object
    Company Response to Consumer    object
    Timely Response                 object
    Consumer Disputed               object
    Complaint ID                     int64
    dtype: object




```python
from datetime import datetime
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
```


```python
df_types = pd.read_csv('P9-ConsumerComplaints.csv', parse_dates=['Date Received'], date_parser=dateparse)
```

    /home/amargaev/tools/anaconda3/lib/python3.8/site-packages/IPython/core/interactiveshell.py:3071: DtypeWarning: Columns (5,11) have mixed types.Specify dtype option on import or set low_memory=False.
      has_raised = await self.run_ast_nodes(code_ast.body, cell_name,



```python
df_types.shape

```




    (65499, 18)




```python
df_types.dtypes
```




    Date Received                   datetime64[ns]
    Product Name                            object
    Sub Product                             object
    Issue                                   object
    Sub Issue                               object
    Consumer Complaint Narrative            object
    Company Public Response                 object
    Company                                 object
    State Name                              object
    Zip Code                                object
    Tags                                    object
    Consumer Consent Provided               object
    Submitted via                           object
    Date Sent to Company                    object
    Company Response to Consumer            object
    Timely Response                         object
    Consumer Disputed                       object
    Complaint ID                             int64
    dtype: object




```python
types = pd.DataFrame([df_types.iloc[:,i].apply(type).value_counts() for i in range(df.shape[1])])
types
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>&lt;class 'pandas._libs.tslibs.timestamps.Timestamp'&gt;</th>
      <th>&lt;class 'str'&gt;</th>
      <th>&lt;class 'float'&gt;</th>
      <th>&lt;class 'int'&gt;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Date Received</th>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Product Name</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Sub Product</th>
      <td>NaN</td>
      <td>46935.0</td>
      <td>18564.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Issue</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Sub Issue</th>
      <td>NaN</td>
      <td>30658.0</td>
      <td>34841.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Consumer Complaint Narrative</th>
      <td>NaN</td>
      <td>2614.0</td>
      <td>62885.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Company Public Response</th>
      <td>NaN</td>
      <td>2450.0</td>
      <td>63049.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Company</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>State Name</th>
      <td>NaN</td>
      <td>65021.0</td>
      <td>478.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Zip Code</th>
      <td>NaN</td>
      <td>65021.0</td>
      <td>478.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Tags</th>
      <td>NaN</td>
      <td>9681.0</td>
      <td>55818.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Consumer Consent Provided</th>
      <td>NaN</td>
      <td>4760.0</td>
      <td>60739.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Submitted via</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Date Sent to Company</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Company Response to Consumer</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Timely Response</th>
      <td>NaN</td>
      <td>65499.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Consumer Disputed</th>
      <td>NaN</td>
      <td>64391.0</td>
      <td>1108.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Complaint ID</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>65499.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
x = df_types.iloc[65497, 4]
print(x)
print(type(x))
```

    Debt is not mine
    <class 'str'>



```python
df.isna().sum()
```




    Date Received                       0
    Product Name                        0
    Sub Product                     18564
    Issue                               0
    Sub Issue                       34841
    Consumer Complaint Narrative    62885
    Company Public Response         63049
    Company                             0
    State Name                        478
    Zip Code                          478
    Tags                            55818
    Consumer Consent Provided       60739
    Submitted via                       0
    Date Sent to Company                0
    Company Response to Consumer        0
    Timely Response                     0
    Consumer Disputed                1108
    Complaint ID                        0
    dtype: int64




```python
df_types.loc[:, 'Sub Issue'].isna().sum()
```




    34841




```python
types.idxmax(axis=1)
```




    Date Received                   <class 'pandas._libs.tslibs.timestamps.Timesta...
    Product Name                                                        <class 'str'>
    Sub Product                                                         <class 'str'>
    Issue                                                               <class 'str'>
    Sub Issue                                                         <class 'float'>
    Consumer Complaint Narrative                                      <class 'float'>
    Company Public Response                                           <class 'float'>
    Company                                                             <class 'str'>
    State Name                                                          <class 'str'>
    Zip Code                                                            <class 'str'>
    Tags                                                              <class 'float'>
    Consumer Consent Provided                                         <class 'float'>
    Submitted via                                                       <class 'str'>
    Date Sent to Company                                                <class 'str'>
    Company Response to Consumer                                        <class 'str'>
    Timely Response                                                     <class 'str'>
    Consumer Disputed                                                   <class 'str'>
    Complaint ID                                                        <class 'int'>
    dtype: object




```python
df_types.loc[df_types['Product Name'] == 'Prepaid card'].loc[:, 'Timely Response'].loc[df_types['Timely Response'] == 'Yes'].count()
```




    186




```python
df_types.loc[:, 'Issue'].isna().sum()
```




    0




```python

```
