import random, json, os
from glob import glob
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
from .. import db, Experiment, Trial, TestAnswer, TrialResponse, QualificationResults, program_versions, program_bases, basic_auth
from grading import grade_string

# ----------------------------------------------------------------------------

mod = Blueprint("core", __name__)

PROG_LANGUAGES = sorted(["C", "Java", "PHP", "JavaScript", "C++",
    "Python", "Ruby", "Objective C", "C#", "SQL", "Perl",
    "Visual Basic", "Haskell", "Lisp", "Erlang",
    "OCaml", "Scheme", "Scala"])

PRE_SURVEY_QS = ["age", "gender", "py_years", "prog_years",
                 "languages", "lang_used", "degree", "cs_major"]

POST_SURVEY_QS = ["difficulty", "guess_correct", "feedback"]

EXPERIMENT_MINUTES = 30
PROGRAM_OUTPUT_DIR = os.path.join("programs", "output")

def fname_noext(path):
    return os.path.splitext(os.path.split(path)[1])[0]

program_output = {}

for p in glob(os.path.join(PROGRAM_OUTPUT_DIR, "*.txt")):
    # Strip .txt off the end
    program_output[fname_noext(p[:-4])] = open(p, "r").read()

def get_experiment():
    assert "experiment_id" in session, "Missing experiment id"
    exp_id = int(session["experiment_id"])
    return Experiment.query.get(exp_id)

def shuffled(xs):
    return sorted(xs, key=lambda x: random.random())

def grade_category(g):
    if g == "exact":
        return "success"
    elif g == "lines":
        return "info"
    elif g == "values":
        return "default"
    else:
        return "warning"

def check_qualification(worker_id):
    qr = QualificationResults.query.filter(QualificationResults.worker_id == worker_id).first()
    return qr is not None and qr.result == "pass"

# ----------------------------------------------------------------------------

QUAL_MINUTES = 5
QUAL_QUESTIONS = {
    "Variables" : "How do you declare a variable?",
    "Functions" : "How do you declare a function?",
    "Printing" : "How do you print \"hellohello\" to the console?",
    "Lists" : "How do you build lists?",
    "Loops" : "How do you print the items in a list?"
}

QUAL_ANSWERS = {
    "Variables": ["int x = 7", "x = 7", "x <- 7", "x == 7"],
    "Functions": ["f(x: int): int =<br />&nbsp;&nbsp;return x + 1",
                  "def f(x):<br />return x + 1",
                  "int f(int x) {<br />&nbsp;&nbsp;&nbsp;&nbsp;return x + 1;<br />}",
                 "def f(x):<br />&nbsp;&nbsp;&nbsp;&nbspreturn x + 1"],
    "Printing": ["System.out.println(\"hello\", \"hello\");",
                 "print \"hello\"<br />print \"hello\"",
                 "System.out.println(\"hello\");<br />System.out.println(\"hello\");",
                 "print \"hello\", \"hello\""],
    "Lists": ["x = []<br />x.append(5)",
              "x = new list()<br />x.add(5)",
              "ArrayList x;<br />x.add(5);",
              "ArrayList x = new ArrayList();<br />x.add(5);"],
    "Loops": ["for x in [1, 2, 3]:<br />&nbsp;&nbsp;&nbsp;&nbsp;print x",
              "int[] list = new int[] { 1, 2, 3 };<br />for (int i = 0; i < list.length; i++)<br />&nbsp;&nbsp;&nbsp;&nbsp;System.out.println(x[i]);",
              "foreach (x: int in [1, 2, 3])<br />&nbsp;&nbsp;&nbsp;&nbsp;print x",
              "int[] list = new int[] { 1, 2, 3 };<br />list.each(x => System.out.println(x));"]
}

QUAL_CORRECT = {
    "Variables" : 1,
    "Functions" : 3,
    "Printing" : 3,
    "Lists" : 0,
    "Loops" : 0
}

@mod.route("/qualification", methods=["GET", "POST"])
def qualification():
    if request.method == "POST":
        # Submitting answers
        assert "worker_id" in session, "Missing worker id"
        worker_id = session["worker_id"]
        assert len(worker_id) > 0, "Empty worker id"

        # Check for duplicate response
        qr = QualificationResults.query.filter(QualificationResults.worker_id == worker_id).first()
        assert qr is not None and qr.started is not None, "Missing or not started"
        assert qr.ended is None and qr.result is None, "Already submitted"
        qr.ended = datetime.now()

        result = "pass"

        # Check time limit and answers
        qual_sec = (qr.ended - qr.started).total_seconds()
        if qual_sec > (QUAL_MINUTES * 60):
            result = "timeout"
        else:
            # Check answers
            for q in QUAL_QUESTIONS.keys():
                assert q in request.form, "Missing question {0}".format(q)
                answer = int(request.form[q])
                if answer != QUAL_CORRECT[q]:
                    result = "fail"
                    break

        # Save result
        qr.result = result
        db.session.commit()

        session.clear()
        return render_template("core/qual-results.html", result=result)
    else:
        # Taking test
        assert "worker_id" in request.args, "Missing worker id"
        worker_id = request.args["worker_id"]
        session["worker_id"] = worker_id

        # Look up or create qualification
        qr = QualificationResults.query.filter(QualificationResults.worker_id == worker_id).first()
        if qr is None:
            # Create qualification result
            qr = QualificationResults(worker_id, "python", datetime.now())
            db.session.add(qr)
            db.session.commit()
        elif qr.result is not None:
            # Test already taken
            flash("You have already taken the test! Result: {0}".format(qr.result),
                category="info")
            return render_template("core/empty.html")

        qual_max_time = timedelta(minutes=QUAL_MINUTES)
        time_left = qual_max_time - (datetime.now() - qr.started)

        # Check time limit
        if time_left.total_seconds() < 0:
            flash("Time limit has been exceeded. You will not be able to complete the experiment.",
                category="danger")
            return render_template("core/empty.html")
        else:
            # Calculate time remaining
            min_left = int(time_left.total_seconds() / 60)
            sec_left = int((time_left - timedelta(seconds=min_left * 60)).total_seconds())

        # Randomize question and answer order
        q_names = shuffled(QUAL_QUESTIONS.keys())
        q_answers = { k : list(shuffled(enumerate(v))) for k, v in QUAL_ANSWERS.iteritems() }
        return render_template("core/qualification.html", q_names=q_names,
                questions=QUAL_QUESTIONS, answers=q_answers, worker_id=worker_id,
                min_left=min_left, sec_left=sec_left)

# ----------------------------------------------------------------------------

@mod.route("/")
def index():
    if "worker_id" in request.values:
        # User is from Mechanical Turk
        worker_id = request.values["worker_id"]

        if not check_qualification(worker_id):
            flash("You must pass the qualification test before taking the experiment!",
                category="danger")
            return render_template("core/empty.html")

        hit_id = request.values["hit_id"]
        submit_to = request.values["submit_to"]
        assignment_id = request.values["assignment_id"]
        return render_template("core/consent.html", worker_id=worker_id,
            hit_id=hit_id, submit_to=submit_to, assignment_id=assignment_id)
    else:
        return render_template("core/consent.html")

@mod.route("/pre-survey", methods=["GET", "POST"])
def pre_survey():
    session.clear()
    if "worker_id" in request.values:
        # User is from Mechanical Turk
        worker_id = request.values["worker_id"]

        # Make sure they passed the qualification
        if not check_qualification(worker_id):
            flash("You must pass the qualification test before taking the experiment!",
                category="danger")
            return render_template("core/empty.html")

        # Make sure they haven't done the experiment before
        duplicate_exp = Experiment.query.filter(Experiment.mt_worker_id == worker_id).first()
        if duplicate_exp is not None:
            flash("You have already started an experiment!", category="danger")
            return render_template("core/empty.html")

        # Pass MT values through to experiment page
        hit_id = request.values["hit_id"]
        submit_to = request.values["submit_to"]
        assignment_id = request.values["assignment_id"]
        return render_template("core/pre-survey.html", langs=PROG_LANGUAGES,
            worker_id=worker_id, hit_id=hit_id, submit_to=submit_to,
            assignment_id=assignment_id)
    else:
        return render_template("core/pre-survey.html", langs=PROG_LANGUAGES)

@mod.route("/post-survey")
def post_survey():
    exp = get_experiment()
    assert exp.trials_completed(), "All trials have not been completed"
    return render_template("core/post-survey.html", exp=exp)

@mod.route("/experiment", methods=["GET", "POST"])
def experiment():
    exp_max_time = timedelta(minutes=EXPERIMENT_MINUTES)
    time_left = exp_max_time

    if "experiment_id" not in session:
        # Create new experiment
        exp = Experiment()
        exp.started = datetime.now()
        exp.user_agent = request.headers.get("User-Agent")
        exp.remote_ip = request.remote_addr

        if "worker_id" in request.form:
            # Make sure user hasn't already taken the experiment
            worker_id = request.form["worker_id"]
            duplicate_exp = Experiment.query.filter(Experiment.mt_worker_id == worker_id).first()
            if duplicate_exp is not None:
                flash("You have already started an experiment!", category="danger")
                return render_template("core/empty.html")

            # User is from Mechanical Turk
            exp.mt_worker_id = worker_id
            exp.mt_hit_id = request.form["hit_id"]
            exp.mt_submit_to = request.form["submit_to"]
            exp.mt_assignment_id = request.form["assignment_id"]
            exp.mt_approved = False

        db.session.add(exp)

        # Create trials (random order, random version)
        for base in shuffled(program_bases):
            version = random.sample(program_versions[base], 1)[0]
            trial = Trial(exp.id, "python", base, version)
            exp.trials.append(trial)

        # Add pre survey answers
        languages = request.form.getlist("languages")
        for q in PRE_SURVEY_QS:
            assert q in request.form, "Missing {0}".format(q)
            if q != "languages":
                ta = TestAnswer(None, q, request.form[q])
                exp.test_answers.append(ta)

        exp.test_answers.append(TestAnswer(None, "languages", ",".join(languages)))

        db.session.commit()
        session["experiment_id"] = exp.id
    else:
        # Look up experiment by id
        exp = get_experiment()
        assert exp.started is not None, "Experiment was not started"

        exp_time = datetime.now() - exp.started
        if exp_time > exp_max_time:
           flash("You have exceeded the maximum amount of time for the experiment.",
                   category="danger")
           return render_template("core/empty.html")

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

    return render_template("core/trial.html", image_path=image_path)

@mod.route("/trial_test")
def trial_test():
    base, version = request.args["b"], request.args["v"]
    image_path = "img/{0}_{1}.png".format(base, version)
    return render_template("core/trial.html", image_path=image_path)

@mod.route("/finish", methods=["POST"])
def finish():
    exp = get_experiment()
    assert exp.ended is None, "Experiment has already been completed"
    print request.form

    # Add post survey answers
    for q in POST_SURVEY_QS:
        assert q in request.form, "Missing {0}".format(q)
        ta = TestAnswer(exp.id, q, request.form[q])
        db.session.add(ta)

    # Complete experiment
    exp.ended = datetime.now()

    # Try auto-grading responses
    for t in exp.trials:
        try:
            prog_name = "{0}_{1}".format(t.program_base, t.program_version)
            expected_output = program_output[prog_name]
            grade = grade_string(expected_output, t.response)

            if grade is not None:
                t.response_grade = grade
        except:
            pass

    db.session.commit()

    session.clear()
    return render_template("core/finish.html", exp=exp, grade_category=grade_category)

# ----------------------------------------------------------------------------

@mod.route("/admin")
@basic_auth.required
def admin():
    session["admin"] = True

    # All experiments
    exps = Experiment.query.order_by(Experiment.started.desc()).all()
    return render_template("core/admin.html", exps=exps)

@mod.route("/approve")
def approve():
    assert "admin" in session and "id" in request.args, "Not logged in or missing id"
    exp = Experiment.query.get(int(request.args["id"]))
    assert exp.is_mt(), "Not a Mechanical Turk experiment"

    # Mark experiment as approved
    exp.mt_approved = True
    db.session.commit()

    flash("Experiment {0} approved".format(exp.id), category="info")
    return redirect(url_for("core.admin"))

@mod.route("/details")
def details():
    assert "admin" in session and "id" in request.args, "Not logged in or missing id"

    # Experiment details
    exp = Experiment.query.get(int(request.args["id"]))
    return render_template("core/details.html", exp=exp,
            grade_category=grade_category, output=program_output)

