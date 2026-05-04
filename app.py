from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os, json, re, requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'zenith_ultra_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zenith.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

db = SQLAlchemy(app)

# ══════════════════════════════════════════════════════════
# MODELS
# ══════════════════════════════════════════════════════════

class User(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(100), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)
    university   = db.Column(db.String(100))
    niche        = db.Column(db.String(100))
    skills       = db.Column(db.String(300))
    bio          = db.Column(db.Text)
    level        = db.Column(db.Integer, default=1)
    xp           = db.Column(db.Integer, default=0)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def skill_list(self):
        return [s.strip() for s in (self.skills or '').split(',') if s.strip()]

    @property
    def rank_label(self):
        if self.level >= 10: return 'Zenith Elite'
        if self.level >= 7:  return 'Innovator'
        if self.level >= 4:  return 'Scholar'
        return 'Initiate'

class Project(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    desc         = db.Column(db.Text)
    ai_tagline   = db.Column(db.String(300))
    xp           = db.Column(db.Integer, default=100)
    world        = db.Column(db.String(50))
    author       = db.Column(db.String(100))
    author_email = db.Column(db.String(100))
    progress     = db.Column(db.Integer, default=0)
    vacancies    = db.Column(db.Integer, default=3)
    tags         = db.Column(db.String(300))
    status       = db.Column(db.String(50), default='Active')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def tag_list(self):
        return [t.strip() for t in (self.tags or '').split(',') if t.strip()]

class PulseActivity(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    actor      = db.Column(db.String(100))
    action     = db.Column(db.String(200))
    project    = db.Column(db.String(200))
    world      = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Connection(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    from_email   = db.Column(db.String(100))
    to_email     = db.Column(db.String(100))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

class ProjectMember(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    project_id   = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_email   = db.Column(db.String(100))
    role         = db.Column(db.String(100), default='Member')
    joined_at    = db.Column(db.DateTime, default=datetime.utcnow)

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

NICHE_WORLD_MAP = {
    'AI/ML': 'tech', 'Full-Stack Dev': 'tech', 'Cloud (Azure)': 'tech',
    'UI/UX Design': 'creative', 'Graphic Design': 'creative', 'Motion Design': 'creative',
    'Research': 'research', 'Biotech': 'research',
    'FinTech': 'economy', 'Blockchain': 'economy',
}

def log_pulse(actor, action, project='', world=''):
    entry = PulseActivity(actor=actor, action=action, project=project, world=world)
    db.session.add(entry)
    db.session.commit()

def groq_chat(prompt, system="You are Zenith AI, assistant for a student collaboration platform."):
    if not GROQ_API_KEY:
        return None
    try:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type': 'application/json'},
            json={
                'model': 'llama3-8b-8192',
                'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}],
                'max_tokens': 300, 'temperature': 0.7
            }, timeout=10
        )
        data = resp.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception:
        return None

def ai_project_dna(title, desc, world):
    prompt = (
        f"Project: '{title}'\nDescription: {desc}\nWorld: {world}\n\n"
        "Return ONLY valid JSON with two keys:\n"
        "1. 'tagline': a punchy 1-sentence tagline (max 15 words) that captures the project DNA.\n"
        "2. 'tags': array of 3 skill/tech tags (strings, max 2 words each).\n"
        'Example: {"tagline": "AI meets civic tech for rural governance.", "tags": ["Python", "ML", "Civic Tech"]}'
    )
    raw = groq_chat(prompt)
    if raw:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return data.get('tagline', ''), ','.join(data.get('tags', []))
        except Exception:
            pass
    return '', ''

def ai_match_score(user_niche, user_skills, project_desc, project_tags, project_world):
    prompt = (
        f"User niche: {user_niche}\nUser skills: {user_skills}\n"
        f"Project description: {project_desc}\nProject tags: {project_tags}\nProject world: {project_world}\n\n"
        'Return ONLY JSON: {"score": <integer 60-99>, "reason": "<one sentence why>"}'
    )
    raw = groq_chat(prompt)
    if raw:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return int(data.get('score', 75)), data.get('reason', '')
        except Exception:
            pass
    combined = f"{project_desc} {project_tags}".lower()
    score = 60
    for skill in (user_skills or '').lower().split(','):
        if skill.strip() and skill.strip() in combined:
            score = min(score + 8, 97)
    return score, 'Based on skill overlap.'

def ai_vibe_match(user_a, user_b):
    prompt = (
        f"Person A: niche={user_a.niche}, skills={user_a.skills}, university={user_a.university}\n"
        f"Person B: niche={user_b.niche}, skills={user_b.skills}, university={user_b.university}\n\n"
        'Return ONLY JSON: {"score": <integer 60-99>, "vibe": "<2-word descriptor like Creative Sync or Tech Twins>"}'
    )
    raw = groq_chat(prompt)
    if raw:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return int(data.get('score', 70)), data.get('vibe', 'Good Match')
        except Exception:
            pass
    return 75, 'Good Match'

def award_xp(email, amount, reason=''):
    user = User.query.filter_by(email=email).first()
    if user:
        user.xp += amount
        user.level = max(1, user.xp // 100)
        db.session.commit()

# ══════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════

@app.route('/')
def index():
    total_users    = User.query.count()
    total_projects = Project.query.count()
    return render_template('index.html', total_users=total_users, total_projects=total_projects)

@app.route('/index.html')
def home():
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name       = request.form.get('name', '').strip()
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        university = request.form.get('university', '').strip()
        skills     = request.form.get('skills', '').strip()
        bio        = request.form.get('bio', '').strip()
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password=generate_password_hash(password),
                    university=university, skills=skills, bio=bio)
        db.session.add(user)
        db.session.commit()
        log_pulse(name, 'joined Zenith', world='all')
        session['user_email'] = email
        session['user_name']  = name
        return redirect(url_for('niche'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user     = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_email'] = email
            session['user_name']  = user.name
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/niche', methods=['GET', 'POST'])
def niche():
    return render_template('niche.html')

@app.route('/save_niche', methods=['POST'])
def save_niche():
    selected = request.form.get('selected_niche', 'AI/ML')
    session['niche'] = selected
    user = User.query.filter_by(email=session.get('user_email')).first()
    if user:
        user.niche = selected
        db.session.commit()
    world_id = NICHE_WORLD_MAP.get(selected, 'tech')
    return redirect(url_for('world_projects', world_id=world_id))

@app.route('/dashboard')
def dashboard():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email = session['user_email']
    user  = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('login'))
    my_projects      = Project.query.filter_by(author_email=email).all()
    memberships      = ProjectMember.query.filter_by(user_email=email).all()
    member_proj_ids  = [m.project_id for m in memberships]
    collab_projects  = Project.query.filter(Project.id.in_(member_proj_ids)).all()
    all_my           = list({p.id: p for p in my_projects + collab_projects}.values())
    stats = {
        'active_projects': len(all_my),
        'xp_this_week':    min(user.xp, 500),
        'collaborators':   User.query.count(),
        'worlds_count':    db.session.query(Project.world).distinct().count(),
    }
    pulse = PulseActivity.query.order_by(PulseActivity.created_at.desc()).limit(5).all()
    conn_emails     = [c.to_email for c in Connection.query.filter_by(from_email=email).limit(5).all()]
    connected_users = User.query.filter(User.email.in_(conn_emails)).all()
    return render_template('dashboard.html',
        user=user, stats=stats, collaborations=all_my[:5],
        pulse=pulse, connected_users=connected_users, unread_count=3)

@app.route('/worlds')
def worlds():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user_email']).first()
    worlds_list = []
    for world_id, label, emoji, desc in [
        ('tech', 'The Tech Hub', '⚡', 'Software, AI, Cloud engineering.'),
        ('creative', 'Creative Studio', '🎨', 'UI/UX, Motion, Branding.'),
        ('research', 'The Lab', '🔬', 'Biotech, Physics, Data Science.'),
        ('economy', 'Economy & Trade', '📈', 'FinTech, Blockchain, Markets.'),
    ]:
        count = Project.query.filter_by(world=world_id).count()
        score, _ = ai_match_score(user.niche or '', user.skills or '', f"{label} {desc}", '', world_id) if user else (80, '')
        worlds_list.append({'id': world_id, 'title': label, 'emoji': emoji,
                            'desc': desc, 'project_count': count, 'match': score})
    worlds_list.sort(key=lambda x: x['match'], reverse=True)
    return render_template('worlds.html', worlds=worlds_list)

@app.route('/world/<world_id>')
def world_projects(world_id):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    projects_list = Project.query.filter_by(world=world_id).order_by(Project.created_at.desc()).all()
    world_names   = {'tech': 'The Tech Hub', 'creative': 'Creative Studio',
                     'research': 'The Lab', 'economy': 'Economy & Trade'}
    return render_template('project_hub.html',
        projects=projects_list,
        world_name=world_names.get(world_id, world_id.title()),
        world_id=world_id)

@app.route('/projects/<path:niche_name>')
def projects(niche_name):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    world_id = NICHE_WORLD_MAP.get(niche_name, 'tech')
    return redirect(url_for('world_projects', world_id=world_id))

@app.route('/project_overview/<int:project_id>')
def project_overview(project_id):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    project = Project.query.get_or_404(project_id)
    members = ProjectMember.query.filter_by(project_id=project_id).all()
    member_users = [User.query.filter_by(email=m.user_email).first() for m in members]
    member_users = [u for u in member_users if u]
    user = User.query.filter_by(email=session['user_email']).first()
    match_score, match_reason = ai_match_score(
        user.niche or '', user.skills or '', project.desc or '', project.tags or '', project.world
    ) if user else (75, '')
    already_member = ProjectMember.query.filter_by(
        project_id=project_id, user_email=session['user_email']).first() is not None
    is_author = project.author_email == session['user_email']
    return render_template('project_overview.html',
        project=project, members=member_users,
        match_score=match_score, match_reason=match_reason,
        already_member=already_member, is_author=is_author)

@app.route('/join_project/<int:project_id>', methods=['POST'])
def join_project(project_id):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email   = session['user_email']
    project = Project.query.get_or_404(project_id)
    existing = ProjectMember.query.filter_by(project_id=project_id, user_email=email).first()
    if not existing:
        db.session.add(ProjectMember(project_id=project_id, user_email=email))
        if project.vacancies > 0:
            project.vacancies -= 1
        db.session.commit()
        award_xp(email, 50, 'Joined project')
        log_pulse(session['user_name'], 'joined', project.title, project.world)
        flash(f'You joined "{project.title}"! +50 XP awarded.')
    else:
        flash('You are already a member of this project.')
    return redirect(url_for('project_overview', project_id=project_id))

@app.route('/propose_project', methods=['GET', 'POST'])
def propose_project_page():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title     = request.form.get('title', '').strip()
        desc      = request.form.get('description', '').strip()
        xp_val    = request.form.get('xp', 100)
        world     = request.form.get('world', 'tech')
        vacancies = int(request.form.get('vacancies', 3))
        tagline, tags = ai_project_dna(title, desc, world)
        project = Project(
            title=title, desc=desc, xp=xp_val, world=world,
            author=session.get('user_name', 'Anonymous'),
            author_email=session['user_email'],
            vacancies=vacancies, progress=0,
            ai_tagline=tagline, tags=tags
        )
        db.session.add(project)
        db.session.commit()
        db.session.add(ProjectMember(project_id=project.id, user_email=session['user_email'], role='Lead'))
        db.session.commit()
        award_xp(session['user_email'], 150, 'Created project')
        log_pulse(session.get('user_name', ''), 'launched', title, world)
        flash('Project launched! AI generated your tagline. +150 XP!')
        return redirect(url_for('my_projects'))
    return render_template('propose_project.html')

@app.route('/propose/<world_id>/', methods=['GET', 'POST'])
def propose_project(world_id):
    if request.method == 'POST':
        return redirect(url_for('world_projects', world_id=world_id))
    return render_template('propose_project.html', world_id=world_id)

@app.route('/my_projects')
def my_projects():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email       = session['user_email']
    owned       = Project.query.filter_by(author_email=email).all()
    memberships = ProjectMember.query.filter_by(user_email=email).all()
    joined_ids  = [m.project_id for m in memberships]
    joined      = Project.query.filter(Project.id.in_(joined_ids), Project.author_email != email).all()
    return render_template('my_projects.html',
        owned_projects=owned, joined_projects=joined,
        author=session.get('user_name'))

@app.route('/collaborators')
def collaborators():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email    = session['user_email']
    me       = User.query.filter_by(email=email).first()
    others   = User.query.filter(User.email != email).all()
    suggestions = []
    for u in others:
        already = Connection.query.filter_by(from_email=email, to_email=u.email).first()
        score, vibe = ai_vibe_match(me, u) if me else (75, 'Good Match')
        suggestions.append({'user': u, 'match': score, 'vibe': vibe, 'connected': already is not None})
    suggestions.sort(key=lambda x: x['match'], reverse=True)
    return render_template('collaborators.html',
        suggestions=suggestions,
        total_collaborators=User.query.count(),
        active_squads=Connection.query.filter_by(from_email=email).count())

@app.route('/initialize_connection/<target_email>')
def initialize_connection(target_email):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email = session['user_email']
    if not Connection.query.filter_by(from_email=email, to_email=target_email).first():
        db.session.add(Connection(from_email=email, to_email=target_email))
        db.session.commit()
        award_xp(email, 20, 'New connection')
        target = User.query.filter_by(email=target_email).first()
        log_pulse(session['user_name'], 'connected with', target.name if target else target_email)
        flash('Connected! +20 XP')
    else:
        flash('Already connected.')
    return redirect(url_for('collaborators'))

@app.route('/archive')
def archive():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    email       = session['user_email']
    owned       = Project.query.filter_by(author_email=email, status='Archived').all()
    memberships = ProjectMember.query.filter_by(user_email=email).all()
    joined_ids  = [m.project_id for m in memberships]
    joined      = Project.query.filter(Project.id.in_(joined_ids), Project.status=='Archived').all()
    all_archived = list({p.id: p for p in owned + joined}.values())
    return render_template('archive.html', archived_projects=all_archived)

@app.route('/archive_project/<int:project_id>', methods=['POST'])
def archive_project(project_id):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    project = Project.query.get_or_404(project_id)
    if project.author_email == session['user_email']:
        project.status   = 'Archived'
        project.progress = 100
        db.session.commit()
        award_xp(session['user_email'], 200, 'Completed project')
        log_pulse(session['user_name'], 'completed', project.title, project.world)
        flash(f'"{project.title}" archived! +200 XP!')
    return redirect(url_for('my_projects'))

@app.route('/messages')
def messages():
    if not session.get('user_email'):
        return redirect(url_for('login'))
    pulse = PulseActivity.query.order_by(PulseActivity.created_at.desc()).limit(20).all()
    return render_template('messages.html', notifications=pulse)

@app.route('/update_progress/<int:project_id>', methods=['POST'])
def update_progress(project_id):
    if not session.get('user_email'):
        return redirect(url_for('login'))
    project = Project.query.get_or_404(project_id)
    if project.author_email == session['user_email']:
        new_val          = int(request.form.get('progress', project.progress))
        project.progress = max(0, min(100, new_val))
        db.session.commit()
        log_pulse(session['user_name'], f'updated progress to {new_val}%', project.title, project.world)
        flash('Progress updated!')
    return redirect(url_for('project_overview', project_id=project_id))

@app.route('/api/pulse')
def api_pulse():
    pulse = PulseActivity.query.order_by(PulseActivity.created_at.desc()).limit(10).all()
    return jsonify([{
        'actor': p.actor, 'action': p.action,
        'project': p.project, 'world': p.world,
        'time': p.created_at.strftime('%H:%M')
    } for p in pulse])

@app.route('/api/squad_suggest/<int:project_id>')
def api_squad_suggest(project_id):
    if not session.get('user_email'):
        return jsonify({'error': 'not logged in'}), 401
    project = Project.query.get_or_404(project_id)
    users   = User.query.filter(User.email != session['user_email']).all()
    ranked  = []
    for u in users:
        score, reason = ai_match_score(
            u.niche or '', u.skills or '', project.desc or '', project.tags or '', project.world)
        ranked.append({'name': u.name, 'niche': u.niche, 'score': score, 'reason': reason})
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(ranked[:5])

@app.route('/overview')
def overview():
    stats = {
        'network_size':       User.query.count(),
        'active_missions':    Project.query.filter_by(status='Active').count(),
        'collaboration_aura': '98%',
        'worlds':             db.session.query(Project.world).distinct().count()
    }
    steps = [
        {'id': '01', 'title': 'Neural Entry',   'desc': 'Register and build your unique scholar profile with skills and bio.'},
        {'id': '02', 'title': 'Explore Worlds', 'desc': 'AI ranks the best project worlds based on your niche and skills.'},
        {'id': '03', 'title': 'Assemble Squad', 'desc': 'AI Vibe Match finds your best collaborators. Build, earn XP, level up.'},
    ]
    return render_template('overview.html', stats=stats, steps=steps)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
