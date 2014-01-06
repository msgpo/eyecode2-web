#!/usr/bin/env python
import sys, os, argparse
sys.path.append(os.getcwd())
sys.path.append('eyecode2')

from eyecode2.app import db, Experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    args = parser.parse_args()

    exp = Experiment.query.get(args.id)
    assert exp is not None, "Experiment not found"
    print "Confirm delete of", exp, "[ENTER]"
    raw_input()
    db.session.delete(exp)
    db.session.commit()
    print "Deleted"
