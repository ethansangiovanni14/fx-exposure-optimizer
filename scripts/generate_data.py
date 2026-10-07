"""Reproducible fictional invoice data for an Excel financial-modeling portfolio project.
No external libraries required. All companies, prices, payments and rates are synthetic.
"""
import csv, random, calendar
from datetime import date, timedelta
from pathlib import Path

R = random.Random(20261006)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'; DATA.mkdir(exist_ok=True)

suppliers = [
('SUP01','Rhein Circuit Components','Germany','EUR','Components','Manufacturing',30,6500,42000,10),
('SUP02','Alpen Precision Systems','Austria','EUR','Equipment','Manufacturing',45,9000,76000,6),
('SUP03','Benelux Sensor Works','Netherlands','EUR','Components','Manufacturing',30,3000,26000,8),
('SUP04','Nordlicht Packaging','Germany','EUR','Packaging','Operations',30,1800,12000,7),
('SUP05','Lyon Industrial Controls','France','EUR','Components','Manufacturing',45,4000,28000,6),
('SUP06','Dublin Systems Licensing','Ireland','EUR','Software','IT',30,950,13000,4),
('SUP07','Milan Assembly Robotics','Italy','EUR','Equipment','Manufacturing',60,12000,85000,4),
('SUP08','Valencia Circuit Supply','Spain','EUR','Components','Manufacturing',30,2500,23000,7),
('SUP09','Thames Electronics Ltd','United Kingdom','GBP','Components','Manufacturing',30,4000,32000,8),
('SUP10','Bristol Calibration Services','United Kingdom','GBP','Services','Operations',45,1000,15000,5),
('SUP11','Manchester Cloud Solutions','United Kingdom','GBP','Software','IT',30,1400,9000,4),
('SUP12','Oxford Technical Materials','United Kingdom','GBP','Components','Manufacturing',60,2500,28000,5),
('SUP13','Osaka Microdevices','Japan','JPY','Components','Manufacturing',45,650000,5500000,9),
('SUP14','Tokyo Automation Systems','Japan','JPY','Equipment','Manufacturing',60,1800000,14000000,5),
('SUP15','Nagoya Logistics Partners','Japan','JPY','Freight','Operations',30,180000,2400000,6),
('SUP16','Kyoto Optical Instruments','Japan','JPY','Components','Manufacturing',30,450000,3800000,8),
('SUP17','Kobe Industrial Packaging','Japan','JPY','Packaging','Operations',45,120000,1400000,6),
('SUP18','Yokohama Engineering Labs','Japan','JPY','Services','Operations',30,300000,2400000,5),
]
headers=['Supplier_ID','Supplier_Name','Country','Currency','Category','Default_Department','Payment_Terms_Days','Typical_Invoice_Min','Typical_Invoice_Max','Relative_Frequency']
with open(DATA/'suppliers.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(headers);w.writerows(suppliers)

# Fictional quarterly planning rates. These are not market-observed rates.
budgets=[]
for year in (2025,2026):
 for quarter in range(1,5):
  budgets.extend([
   (f'{year}-Q{quarter}','EUR',round(1.07+0.018*(quarter-2)+0.013*(year-2025),4)),
   (f'{year}-Q{quarter}','GBP',round(1.26+0.022*(quarter-2)+0.011*(year-2025),4)),
   (f'{year}-Q{quarter}','JPY',round(.0067+0.00014*(quarter-2)-0.0001*(year-2025),6))
  ])
with open(DATA/'budget_rates_synthetic.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Budget_Quarter','Currency','Budget_USD_Per_Unit']);w.writerows(budgets)

def random_day(y,m):
 return date(y,m,R.randint(1,calendar.monthrange(y,m)[1]))

def fmtdate(dt): return dt.isoformat()

months=[(y,m) for y in (2025,2026) for m in range(1,13)]
weights=[s[-1] for s in suppliers]
rows=[]
for i in range(1500):
 y,m=R.choice(months)
 supplier=R.choices(suppliers,weights=weights,k=1)[0]
 sid,name,country,cur,cat,dept,terms,low,high,_=supplier
 amount=round(R.uniform(low,high)*R.choice([0.7,0.9,1,1,1,1.15,1.35]),2)
 when=random_day(y,m)
 due=when+timedelta(days=terms)
 status='Historical' if when<=date(2026,9,30) else 'Planned'
 rows.append({'Invoice_ID':f'INV-{i+1:05d}','Supplier_ID':sid,'Supplier_Name':name,'Department':dept,'Category':cat,'Invoice_Date':fmtdate(when),'Due_Date':fmtdate(due),'Currency':cur,'Invoice_Amount_Local':f'{amount:.2f}','Record_Status':status})
# Diverse, controlled quality anomalies in 105 DISTINCT records (~7%).
selected=R.sample(range(1500),105)
anomaly_counts={'supplier_naming':0,'missing_department':0,'date_format':0,'amount_format':0,'duplicate_invoice_id':0,'category_alias':0,'blank_due_date':0}
for j,ix in enumerate(selected):
 row=rows[ix]
 kind=j%7
 if kind==0:
  row['Supplier_Name']=R.choice([row['Supplier_Name'].upper(),row['Supplier_Name'].lower(),' '+row['Supplier_Name']+'  ']);anomaly_counts['supplier_naming']+=1
 elif kind==1:
  row['Department']='';anomaly_counts['missing_department']+=1
 elif kind==2:
  d=date.fromisoformat(row['Invoice_Date']);row['Invoice_Date']=f'{d.month}/{d.day}/{d.year}';anomaly_counts['date_format']+=1
 elif kind==3:
  val=float(row['Invoice_Amount_Local']);row['Invoice_Amount_Local']=f'{val:,.2f}';anomaly_counts['amount_format']+=1
 elif kind==4:
  # Deliberately duplicated invoice identifier, not necessarily a duplicate transaction.
  row['Invoice_ID']=rows[(ix+97)%1500]['Invoice_ID'];anomaly_counts['duplicate_invoice_id']+=1
 elif kind==5:
  row['Category']={'Components':'Parts','Operations':'Ops','Software':'IT Software','Services':'Service','Equipment':'Equip.','Packaging':'Pack.','Freight':'Shipping'}.get(row['Category'],row['Category']);anomaly_counts['category_alias']+=1
 else:
  row['Due_Date']='';anomaly_counts['blank_due_date']+=1
R.shuffle(rows)
with open(DATA/'supplier_invoices_raw.csv','w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Generated',len(rows),'raw invoice records;',len(suppliers),'suppliers;',len(budgets),'quarterly reference rates')
print('Introduced issues:',anomaly_counts)
print('Historical:',sum(r['Record_Status']=='Historical' for r in rows),'Planned:',sum(r['Record_Status']=='Planned' for r in rows))
