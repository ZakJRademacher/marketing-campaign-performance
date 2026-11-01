"""Missing groups, comparison denominators and calendar-label boundaries."""
import importlib.util
from pathlib import Path
import sqlite3
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('compare_outcomes',ROOT/'tools/compare_outcomes.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class MatchedOutcomeTests(unittest.TestCase):
    def database(self):
        db=sqlite3.connect(':memory:');self.addCleanup(db.close)
        db.execute('CREATE TABLE campaigns(source_row INTEGER,month TEXT,month_order INTEGER,channel TEXT,previous_outcome TEXT,contacts INTEGER,subscribed INTEGER)')
        return db

    def test_correct_group_rates_and_contacts_within_same_cell(self):
        db=self.database()
        db.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?)',[(2,'may',5,'cellular','success',1,1),(3,'may',5,'cellular','success',3,0),(4,'may',5,'cellular','failure',6,0),(5,'may',5,'cellular','nonexistent',2,1)])
        r=m.query(db)[0]
        self.assertEqual((r['all_records'],r['success_records'],r['failure_records'],r['other_outcome_records']),(4,2,1,1))
        self.assertEqual((r['success_rate'],r['failure_rate'],r['observed_rate_gap']),(0.5,0.0,0.5))
        self.assertEqual((r['success_contacts'],r['failure_contacts']),(4,6))
        self.assertIn('below 100',r['population_note'])

    def test_missing_groups_are_retained_without_filled_rates(self):
        db=self.database()
        db.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?)',[(2,'may',5,'telephone','success',1,1),(3,'jun',6,'cellular','failure',2,0),(4,'jul',7,'cellular','nonexistent',1,1)])
        results=m.query(db)
        self.assertEqual(len(results),3)
        self.assertTrue(all(r['observed_rate_gap'] is None for r in results))
        self.assertIsNone(results[0]['failure_rate']);self.assertIsNone(results[1]['success_rate'])
        self.assertEqual(results[2]['comparison_status'],'Neither comparison group observed')

    def test_channels_are_not_pooled_and_month_order_is_not_a_year(self):
        db=self.database()
        db.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?)',[(2,'dec',12,'cellular','success',1,1),(3,'jan',1,'cellular','failure',1,0),(4,'jan',1,'telephone','success',1,1)])
        rows=m.query(db)
        self.assertEqual([r['month'] for r in rows],['jan','jan','dec'])
        self.assertEqual(len({(r['month'],r['channel']) for r in rows}),3)
        self.assertTrue(all(r['comparison_status']!='Both groups observed' for r in rows))


if __name__=='__main__':unittest.main()
