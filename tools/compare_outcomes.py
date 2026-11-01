"""Export within-month/channel prior-outcome comparisons without new dependencies."""
import argparse
import csv
import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def query(db):
    db.row_factory = sqlite3.Row
    return [dict(r) for r in db.execute((ROOT / 'sql/matched_outcomes.sql').read_text(encoding='utf-8'))]


def compare(database, output):
    database, output = Path(database).resolve(), Path(output).resolve()
    if not database.is_file():
        raise FileNotFoundError('Run python tools/download_data.py and python refresh.py first')
    with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as db:
        db.execute('PRAGMA query_only = ON')
        n, distinct = db.execute('SELECT COUNT(*), COUNT(DISTINCT source_row) FROM campaigns').fetchone()
        if n != distinct:
            raise ValueError('Source Row must uniquely identify each campaign observation')
        results = query(db)
        if not results:
            raise ValueError('No campaign observations; no comparison published')
        source = dict(db.execute('SELECT COUNT(*) AS records, SUM(subscribed) AS subscriptions, SUM(contacts) AS contacts FROM campaigns').fetchone())
        actual = {key: sum(r['all_' + key] for r in results) for key in ['records','subscriptions','contacts']}
        outcomes = [dict(r) for r in db.execute('SELECT previous_outcome, COUNT(*) AS records, SUM(subscribed) AS subscriptions, SUM(contacts) AS contacts FROM campaigns GROUP BY previous_outcome ORDER BY previous_outcome')]
        if actual != source:
            raise ValueError('Comparison cells do not reconcile to source totals')
        for outcome in ['success','failure']:
            expected = next((r for r in outcomes if r['previous_outcome']==outcome), {'records':0,'subscriptions':0,'contacts':0})
            if any(sum(r[outcome+'_'+key] for r in results)!=expected[key] for key in ['records','subscriptions','contacts']):
                raise ValueError('Prior-outcome populations do not reconcile')
    output.mkdir(parents=True, exist_ok=True)
    pending = output / 'matched-cells.csv.next'
    with pending.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream,list(results[0]),lineterminator='\n');writer.writeheader();writer.writerows(results)
    pending.replace(output / 'matched-cells.csv')
    controls = {'input_database_sha256':hashlib.sha256(database.read_bytes()).hexdigest(),
                'sql_sha256':hashlib.sha256((ROOT/'sql/matched_outcomes.sql').read_bytes()).hexdigest(),
                'csv_sha256':hashlib.sha256((output/'matched-cells.csv').read_bytes()).hexdigest(),
                'source_totals':source,'result_totals':actual,'source_outcomes':outcomes,
                'observed_month_channel_cells':len(results),
                'cells_with_both_groups':sum(r['comparison_status']=='Both groups observed' for r in results),
                'cells_without_both_groups':sum(r['comparison_status']!='Both groups observed' for r in results),
                'interpretation':'Same observed month and channel only; years are pooled. No client ID, randomized intervention, matched-person effect or causal lift is inferred.',
                'absence':'Zero records means an observed group is absent in this source cell. Its rate and the two-group gap are blank, never filled with zero.'}
    pending = output / 'controls.json.next';pending.write_text(json.dumps(controls,indent=2)+'\n',encoding='utf-8');pending.replace(output/'controls.json')
    return controls


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=ROOT/'data/processed/analysis.sqlite')
    parser.add_argument('--output',type=Path,default=ROOT/'deliverables/outcome-comparison')
    args=parser.parse_args();print(json.dumps(compare(args.database,args.output),indent=2))
