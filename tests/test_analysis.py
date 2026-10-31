from pathlib import Path
import csv,importlib.util,json,sqlite3,unittest
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('refresh',P/'refresh.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CampaignChecks(unittest.TestCase):
    def test_band_boundaries(self):
        self.assertEqual([m.contact_band(x)[:2] for x in [1,2,3,4,5,6,56]],['01','02','03','04','04','05','05'])
        with self.assertRaises(ValueError):m.contact_band(0)
    def test_independent_source_reconciliation(self):
        with (P/'data/raw/bank-additional-full.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter=';'))
        self.assertEqual(len(rows),41188);self.assertEqual(sum(r['y']=='yes' for r in rows),4640)
        self.assertEqual(sum(int(r['campaign']) for r in rows),105754)
    def test_dimension_uniqueness_and_join_grain(self):
        with (P/'data/processed/Campaigns.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        for table,key in [('Months','Month'),('Channels','Channel'),('Outcomes','Previous Outcome'),('ContactBands','Contact Band')]:
            with (P/f'data/processed/{table}.csv').open(encoding='utf-8-sig') as f:dim=list(csv.DictReader(f))
            keys=[r[key] for r in dim];self.assertEqual(len(keys),len(set(keys)))
            self.assertTrue(all(r[key] in keys for r in rows))
        self.assertEqual(len(set(r['Source Row'] for r in rows)),41188)
    def test_filter_intersection(self):
        db=sqlite3.connect(P/'data/processed/analysis.sqlite')
        self.assertEqual(db.execute("SELECT COUNT(*),SUM(subscribed),SUM(contacts) FROM campaigns WHERE channel='cellular' AND month='may'").fetchone(),(5518,614,12488))
        self.assertEqual(db.execute("SELECT COUNT(*) FROM campaigns WHERE channel='nonexistent'").fetchone()[0],0)
    def test_leakage_fields_not_in_report(self):
        model=json.loads((P/'powerbi/CampaignReview.SemanticModel/model.bim').read_text())
        names={c['name'].lower() for t in model['model']['tables'] for c in t['columns']}
        self.assertFalse(names.intersection({'duration','age','job','marital','default','balance','housing','loan'}))

if __name__=='__main__':unittest.main()
