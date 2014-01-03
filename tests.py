import sys, os
sys.path.append(os.getcwd())
sys.path.append('eyecode2')

os.environ["EYECODE2_CONFIG"] = "test.cfg"
from eyecode2.app import app, db, Experiment, Trial, program_versions
import flask
import unittest
import tempfile

NUM_PROGRAMS = 8
DB_PATH = "/tmp/eyecode2_test.db"

class EyecodeTestCases(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        os.unlink(DB_PATH)

    def test_complete(self):
        with app.test_client() as client:

            # Complete pre-survey
            rv = client.post("/experiment", data=dict(
                age="30", cs_major="current",
                degree="masters", gender="male",
                lang_used="Python", languages="Python",
                py_years="5", prog_years="15"
            ))

            assert "Welcome to the eyeCode experiment!" in rv.data
            assert "experiment_id" in flask.session

            exp_id = int(flask.session["experiment_id"])
            exp = Experiment.query.get(exp_id)
            assert exp.started is not None

            # Provide a guess for each program
            rv = None
            for i, t in enumerate(exp.trials):

                # Start trial
                rv = client.get("/trial?n={0}".format(i + 1))
                image_name = "{0}_{1}.png".format(t.program_base, t.program_version)
                assert image_name in rv.data
                assert "trial_id" in flask.session

                t_id = int(flask.session["trial_id"])
                assert t.id == t_id

                t = Trial.query.get(t_id)
                assert t.started is not None and t.ended is None

                # Post trial response
                rv = client.post("/experiment", data=dict(
                    response = "test",
                    responses_js = "[]"
                ), follow_redirects=True)

                t = Trial.query.get(t_id)
                assert t.ended is not None

            # We should be at the post-experiment survey
            assert "Post-Survey" in rv.data
            assert "trial_id" not in flask.session

            # The experiment should have all trials completed
            exp = Experiment.query.get(exp_id)
            assert exp.trials_completed()

            # Complete post-survey
            rv = client.post("/finish", data=dict(
                difficulty="easy",
                guess_correct="most",
                feedback="test"
            ))

            # We should be at the finish page with the session cleared
            assert "Thank you for completing the experiment" in rv.data
            assert "experiment_id" not in flask.session

            # Experiment should be done
            exp = Experiment.query.get(exp_id)
            assert exp.ended is not None

    def test_images(self):
        # Make sure an image exists for every base/version
        image_dir = os.path.join("eyecode2", "app", "static", "img")
        for b, vs in program_versions.iteritems():
            for v in vs:
                image_path = os.path.join(image_dir, "{0}_{1}.png".format(b, v))
                assert os.path.exists(image_path), image_path


if __name__ == '__main__':
    unittest.main()
