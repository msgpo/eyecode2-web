import os, time
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("app.config")

if "EYECODE2_CONFIG" in os.environ:
    app.config.from_envvar("EYECODE2_CONFIG")

db = SQLAlchemy(app)

# --------------------------------------------------

class Experiment(db.Model):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    started = Column(DateTime)
    ended = Column(DateTime)
    created = Column(DateTime)
    remote_ip = Column(Text)
    user_agent = Column(Text)

    mt_hit_id = Column(Text)
    mt_assignment_id = Column(Text)
    mt_worker_id = Column(Text)
    mt_submit_to = Column(Text)
    mt_approved = Column(Boolean)

    def __init__(self, started=None, ended=None):
        self.created = datetime.now()
        self.started = started
        self.ended = ended
        self.mt_approved = False

    def __repr__(self):
        return "<Experiment({0}, {1}, {2})>".format(self.id, self.started, self.mt_hit_id)

    def is_mt(self):
        return (self.mt_hit_id is not None) and (len(self.mt_hit_id) > 0)

    def trials_completed(self):
        return all(t.started is not None for t in self.trials)

    def mt_code(self):
        timestamp = int(time.mktime(self.started.timetuple()))
        code = (timestamp * self.id) ^ timestamp
        return code

    def valid_code(self, code):
        timestamp = int(time.mktime(self.started.timetuple()))
        return timestamp == ((code ^ timestamp) / self.id)

# --------------------------------------------------

class TestAnswer(db.Model):
    __tablename__ = "test_answers"

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    created = Column(DateTime)

    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", backref=backref("test_answers", order_by=id))

    def __init__(self, experiment_id, question, answer):
        self.experiment_id = experiment_id
        self.question = question
        self.answer = answer
        self.created = datetime.now()

    def __repr__(self):
        return "<TestAnswer({0}, {1}, {2})>".format(self.id, self.question, self.answer)

# --------------------------------------------------

class Trial(db.Model):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True)
    language = Column(Text)
    program_base = Column(Text)
    program_version = Column(Text)
    response = Column(Text)
    response_grade = Column(Text)
    started = Column(DateTime)
    ended = Column(DateTime)
    restarted = Column(Integer)
    created = Column(DateTime)

    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", backref=backref("trials", order_by=id))

    def __init__(self, experiment_id, language, program_base, program_version,
            response=None, started=None, ended=None):

        self.experiment_id = experiment_id
        self.language = language
        self.program_base = program_base
        self.program_version = program_version
        self.created = datetime.now()
        self.response = response
        self.started = started
        self.ended = ended
        self.restarted = 0

    def __repr__(self):
        return "<Trial({0}, {1}, {2}_{3})>".format(self.id, self.experiment_id,
                self.program_base, self.program_version)

    def language_ext(self):
        if self.language == "python":
            return "py"
        elif self.language == "java":
            return "java"

        raise ValueError("Unsupported language {0}".format(self.language))

# --------------------------------------------------

class TrialResponse(db.Model):
    __tablename__ = "trial_responses"

    id = Column(Integer, primary_key=True)
    response = Column(Text)
    timestamp = Column(BigInteger)
    created = Column(DateTime)

    trial_id = Column(Integer, ForeignKey("trials.id"))
    trial = relationship("Trial", backref=backref("responses", order_by=id))

    def __init__(self, trial_id, response, timestamp):
        self.trial_id = trial_id
        self.created = datetime.now()
        self.response = response
        self.timestamp = timestamp

    def __repr__(self):
        return "<TrialResponse({0}, {1}, {2})>".format(self.id, self.trial_id, self.timestamp)

# --------------------------------------------------

class QualificationResults(db.Model):
    __tablename__ = "qualification_results"

    id = Column(Integer, primary_key=True)
    worker_id = Column(Text)
    language = Column(Text)
    result = Column(Text)
    started = Column(DateTime)
    ended = Column(DateTime)
    created = Column(DateTime)

    def __init__(self, worker_id, language, started, ended, result):
        self.worker_id = worker_id
        self.language = language
        self.started = started
        self.ended = ended
        self.result = result
        self.created = datetime.now()

    def __repr__(self):
        return "<QualificationResults({0}, {1}, {2})>".format(self.id, self.worker_id, self.result)

# --------------------------------------------------

program_versions = {
    "basketball" : ["iterative", "recursive"],
    "between"    : ["functions", "inline"],
    "counting"   : ["done", "other"],
    "order"      : ["inorder", "shuffled"],
    "overload"   : ["numbers", "words"],
    "rectangle"  : ["long", "short"],
    "scope"      : ["justreturn", "noreturn", "return"],
    "whitespace" : ["normal", "nospace", "nospace_highlight"]
}

program_bases = program_versions.keys()

# --------------------------------------------------

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

from app.core.views import mod as core
app.register_blueprint(core)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)

