"""Prepare the full UCI campaign snapshot without demographic targeting fields."""
from pathlib import Path
import csv,hashlib,json,sqlite3

ROOT=Path(__file__).resolve().parent
MONTHS=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

def contact_band(n):
    if n<1:raise ValueError('Campaign contacts must be positive')
    return '01  One contact' if n==1 else '02  Two contacts' if n==2 else '03  Three contacts' if n==3 else '04  Four-five contacts' if n<=5 else '05  Six+ contacts'

def refresh(root=ROOT):
    source=root/'data/raw/bank-additional-full.csv';meta=json.loads((root/'data/source-download.json').read_text())
    expected=next(x['sha256'] for x in meta['files'] if x['name']==source.name)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==expected,'Source fingerprint changed; review before publication'
    output=root/'data/processed';output.mkdir(parents=True,exist_ok=True)
    records=[];seen=set();repeats=0
    with source.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream,delimiter=';');assert len(reader.fieldnames)==len(set(reader.fieldnames))
        for rowno,row in enumerate(reader,2):
            assert None not in row and None not in row.values()
            raw=tuple(row.values());repeats+=raw in seen;seen.add(raw)
            n=int(row['campaign']);band=contact_band(n);assert row['y'] in ('yes','no')
            month=row['month'];assert month in MONTHS
            outcome=row['poutcome'].strip() or 'unknown';channel=row['contact'].strip() or 'unknown'
            records.append((rowno,month,MONTHS.index(month)+1,channel,outcome,n,band,int(row['y']=='yes')))
    assert len(records)==41188
    db=sqlite3.connect(':memory:');db.execute('CREATE TABLE campaigns(source_row INTEGER PRIMARY KEY,month TEXT,month_order INTEGER,channel TEXT,previous_outcome TEXT,contacts INTEGER,contact_band TEXT,subscribed INTEGER)')
    db.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?,?)',records)
    with (output/'Campaigns.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.writer(stream);w.writerow(['Source Row','Month','Month Order','Channel','Previous Outcome','Contacts','Contact Band','Subscribed']);w.writerows(records)
    # Dimensions retain all observed levels and use deterministic text keys.
    dims=[('Months','SELECT DISTINCT month,month_order FROM campaigns ORDER BY month_order',['Month','Month Order']),('Channels','SELECT DISTINCT channel FROM campaigns ORDER BY channel',['Channel']),('Outcomes','SELECT DISTINCT previous_outcome FROM campaigns ORDER BY previous_outcome',['Previous Outcome']),('ContactBands','SELECT DISTINCT contact_band FROM campaigns ORDER BY contact_band',['Contact Band'])]
    for name,query,headers in dims:
        with (output/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as s:
            w=csv.writer(s);w.writerow(headers);w.writerows(db.execute(query))
    controls={}
    for key,where in [('all','1=1'),('cellular',"channel='cellular'"),('may',"month='may'"),('success',"previous_outcome='success'"),('cellular_may',"channel='cellular' AND month='may'")]:
        n,y,c=db.execute('SELECT COUNT(*),SUM(subscribed),SUM(contacts) FROM campaigns WHERE '+where).fetchone()
        controls[key]={'records':n,'subscriptions':y,'conversion':y/n,'recorded_contacts':c,'subscriptions_per_100_contacts':100*y/c}
    for group in ['contact_band','previous_outcome','channel','month']:
        cur=db.execute(f'SELECT {group},COUNT(*) records,SUM(subscribed) subscriptions,1.0*SUM(subscribed)/COUNT(*) conversion,SUM(contacts) recorded_contacts FROM campaigns GROUP BY {group} ORDER BY conversion DESC')
        with (output/(group+'-summary.csv')).open('w',newline='',encoding='utf-8') as s:
            w=csv.writer(s);w.writerow([x[0] for x in cur.description]);w.writerows(cur)
    cur=db.execute('SELECT month,channel,previous_outcome,contact_band,COUNT(*) records,SUM(subscribed) subscriptions,SUM(contacts) recorded_contacts FROM campaigns GROUP BY month,channel,previous_outcome,contact_band')
    with (output/'comparison-cells.csv').open('w',newline='',encoding='utf-8') as s:
        w=csv.writer(s);w.writerow([x[0] for x in cur.description]);w.writerows(cur)
    controls.update(source_rows=len(records),exact_repeats_retained=repeats,source_sha256=expected,reporting_sha256=hashlib.sha256((output/'Campaigns.csv').read_bytes()).hexdigest())
    (output/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    temp=output/'analysis.next.sqlite';db.commit();dest=sqlite3.connect(temp);db.backup(dest);dest.close();temp.replace(output/'analysis.sqlite')
    print(json.dumps(controls,indent=2));return controls

if __name__=='__main__':refresh()
