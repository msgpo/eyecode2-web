import random, json, os
from glob import glob
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
from .. import db, Experiment, Trial, TestAnswer, TrialResponse, program_versions, program_bases
from grading import grade_string

# ----------------------------------------------------------------------------

mod = Blueprint("core", __name__)

PROG_LANGUAGES = sorted(["C", "Java", "PHP", "JavaScript", "C++",
    "Python", "Ruby", "Objective C", "C#", "SQL", "Perl",
    "Visual Basic", "Haskell", "Lisp", "Erlang",
    "OCaml", "Scheme", "Scala"])

EXPERIMENT_MINUTES = 45
PROGRAM_OUTPUT_DIR = os.path.join("programs", "output")

def fname_noext(path):
    return os.path.splitext(os.path.split(path)[1])[0]

program_output = { fname_noext(p): open(p, "r").read()
                   for p in glob(os.path.join(PROGRAM_OUTPUT_DIR, "*.txt")) }

def get_experiment():
    assert "experiment_id" in session
    exp_id = int(session["experiment_id"])
    return Experiment.query.get(exp_id)

# ----------------------------------------------------------------------------

@mod.route("/")
def index():
    return render_template("core/consent.html")

@mod.route("/pre-survey")
def pre_survey():
    session.clear()
    return render_template("core/pre-survey.html", langs=PROG_LANGUAGES)

@mod.route("/post-survey")
def post_survey():
    exp = get_experiment()
    assert exp.trials_completed(), "All trials have not been completed"
    return render_template("core/post-survey.html", exp=exp)

@mod.route("/experiment", methods=["GET", "POST"])
def experiment():
    # DEBUG
    #if "xxyx" in request.form:
        #session["experiment_id"] = int(request.form["xxyx"])
    # DEBUG

    exp_max_time = timedelta(minutes=EXPERIMENT_MINUTES)
    time_left = exp_max_time

    if "experiment_id" not in session:
        # Create new experiment
        exp = Experiment()
        exp.started = datetime.now()
        exp.user_agent = request.headers.get("User-Agent")
        exp.remote_ip = request.remote_addr
        db.session.add(exp)

        # Create trials (random order, random version)
        for base in sorted(program_bases, key=lambda x: random.random()):
            version = random.sample(program_versions[base], 1)[0]
            trial = Trial(exp.id, "python", base, version)
            exp.trials.append(trial)

        # Add pre survey answers
        languages = request.form.getlist("languages")
        for k,v in request.form.iteritems():
            if k != "languages":
                ta = TestAnswer(None, k, v)
                exp.test_answers.append(ta)

        exp.test_answers.append(TestAnswer(None, "languages", ",".join(languages)))

        db.session.commit()
        session["experiment_id"] = exp.id
    else:
        # Look up experiment by id
        exp = get_experiment()
        assert exp.started is not None, "Experiment was not started"

        exp_time = datetime.now() - exp.started
        assert exp_time < exp_max_time, "No more time for experiment"
        time_left = exp_max_time - exp_time

        if "trial_id" in session:
            # Clear from session
            trial_id = session.pop("trial_id")

            if "response" in request.form:
                # End trial
                trial = Trial.query.get(trial_id)

                assert trial.started is not None, "Trial was not started"
                trial.ended = datetime.now()
                trial.response = request.form["response"]

                # Add intermediary responses
                for date, response in json.loads(request.form["responses_js"]):
                    tr = TrialResponse(trial.id, response, date)
                    db.session.add(tr)

                db.session.commit()

        # Check if experiment is finished
        if exp.trials_completed():
            return redirect(url_for("core.post_survey"))

    min_left = int(time_left.total_seconds() / 60)
    sec_left = int((time_left - timedelta(seconds=min_left * 60)).total_seconds())
    return render_template("core/experiment.html", exp=exp, min_left=min_left,
            sec_left=sec_left)

@mod.route("/trial")
def trial():
    assert "n" in request.args, "Trial number is required"
    exp = get_experiment()

    # Load trial n
    trial_num = int(request.args.get("n"))
    if trial_num is None or trial_num < 1 \
            or trial_num > len(exp.trials):
        return redirect(url_for("core.experiment"))

    # Start trial
    trial = exp.trials[trial_num - 1]
    assert trial.started is None, "Trial has already been started"
    trial.started = datetime.now()
    db.session.commit()

    session["trial_id"] = trial.id
    image_path = "img/{0}_{1}.png".format(trial.program_base, trial.program_version)

    return render_template("core/trial.html", trial=trial, image_path=image_path)

@mod.route("/finish", methods=["POST"])
def finish():
    exp = get_experiment()
    assert exp.ended is None, "Experiment has already been completed"

    # Add post survey answers
    for k,v in request.form.iteritems():
        ta = TestAnswer(exp.id, k, v)
        db.session.add(ta)

    # Complete experiment
    exp.ended = datetime.now()

    # Try auto-grading responses
    for t in exp.trials:
        try:
            prog_name = "{0}_{1}.py".format(t.program_base, t.program_version)
            expected_output = program_output[prog_name]
            grade = grade_string(expected_output, t.response)

            if grade is not None:
                t.response_grade = grade
        except:
            pass

    db.session.commit()

    session.clear()
    return render_template("core/finish.html", exp=exp)
