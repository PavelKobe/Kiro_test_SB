from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from forms import ContactForm, LoginForm, IncidentForm
from functools import wraps
from datetime import datetime
import sys
import os

# Добавляем путь к моделям Stockmann
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
from stockmann_models import (
    db, Store, Department, User, IncidentCategory, IncidentSubcategory, 
    Incident, IncidentHistory, IncidentComment
)

app = Flask(__name__)
app.config.from_object(Config)

# Переопределяем настройки БД для Stockmann
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Инициализация базы данных
db.init_app(app)
migrate = Migrate(app, db)

# Словарь пользователей (логин: пароль)
users = {
    'admin': '12345',
    'manager': 'password',
    'user': '123456'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Необходимо войти в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request.form)
        
        if form.validate():
            username = form.username
            password = form.password
            
            if username in users and users[username] == password:
                session['logged_in'] = True
                session['username'] = username
                session['login_time'] = datetime.now().strftime('%d.%m.%Y %H:%M')
                
                # Пытаемся найти пользователя в БД
                try:
                    db_user = User.query.filter_by(username=username).first()
                    if db_user:
                        session['user_id'] = db_user.id
                        session['user_role'] = db_user.role
                        session['store_id'] = db_user.store_id
                    else:
                        session['user_id'] = 1  # Fallback для тестирования
                        session['user_role'] = 'admin'
                except:
                    session['user_id'] = 1
                    session['user_role'] = 'admin'
                
                flash(f'Добро пожаловать, {username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неверный логин или пароль', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

@app.route('/incidents')
@login_required
def incidents():
    # Получаем статистику инцидентов
    total_incidents = Incident.query.count()
    active_incidents = Incident.query.filter(Incident.status.in_(['new', 'assigned', 'in_progress'])).count()
    resolved_incidents = Incident.query.filter_by(status='resolved').count()
    overdue_incidents = Incident.query.filter(
        Incident.sla_deadline < datetime.utcnow(),
        Incident.status.notin_(['resolved', 'closed', 'cancelled'])
    ).count()
    
    # Получаем последние инциденты
    recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(10).all()
    
    return render_template('incidents.html', 
                         total_incidents=total_incidents,
                         active_incidents=active_incidents,
                         resolved_incidents=resolved_incidents,
                         overdue_incidents=overdue_incidents,
                         recent_incidents=recent_incidents)

@app.route('/incidents/create', methods=['GET', 'POST'])
@login_required
def create_incident():
    form = IncidentForm()
    
    # Загружаем данные для селектов
    stores = Store.query.filter_by(is_active=True).all()
    categories = IncidentCategory.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        form = IncidentForm(request.form)
        
        if form.validate():
            try:
                # Генерируем номер инцидента
                store = Store.query.get(int(form.store_id)) if form.store_id else None
                if store:
                    # Получаем текущий год
                    from datetime import datetime
                    current_year = datetime.now().year
                    
                    # Ищем последний номер для данного магазина и года
                    last_incident = db.session.query(Incident).filter(
                        Incident.incident_number.like(f"{store.code}-{current_year}-%")
                    ).order_by(Incident.incident_number.desc()).first()
                    
                    if last_incident and last_incident.incident_number:
                        # Извлекаем номер из строки типа "HEL001-2025-0001"
                        parts = last_incident.incident_number.split('-')
                        if len(parts) >= 3:
                            try:
                                last_num = int(parts[-1])
                                next_num = last_num + 1
                            except ValueError:
                                next_num = 1
                        else:
                            next_num = 1
                    else:
                        next_num = 1
                    
                    # Формируем номер инцидента
                    incident_number = f"{store.code}-{current_year}-{next_num:04d}"
                else:
                    # Если магазин не выбран, используем общий формат
                    incident_number = f"GEN-{datetime.now().year}-{datetime.now().strftime('%m%d%H%M%S')}"
                
                # Создаем новый инцидент
                incident = Incident(
                    incident_number=incident_number,
                    title=form.title,
                    description=form.description,
                    category_id=int(form.category_id) if form.category_id else None,
                    subcategory_id=int(form.subcategory_id) if form.subcategory_id else None,
                    priority=form.priority,
                    severity=form.severity,
                    store_id=int(form.store_id) if form.store_id else None,
                    department_id=int(form.department_id) if form.department_id else None,
                    location_details=form.location_details,
                    reporter_id=session.get('user_id', 1),  # ID текущего пользователя
                    assigned_to=int(form.assigned_to) if form.assigned_to else None,
                    customer_affected=form.customer_affected == 'true',
                    source='manual'
                )
                
                # Устанавливаем время создания явно
                incident.created_at = datetime.utcnow()
                incident.updated_at = datetime.utcnow()
                
                db.session.add(incident)
                db.session.commit()
                
                # Рассчитываем SLA если есть подкатегория
                if form.subcategory_id:
                    subcategory = IncidentSubcategory.query.get(int(form.subcategory_id))
                    if subcategory:
                        from datetime import timedelta
                        incident.sla_deadline = incident.created_at + timedelta(hours=subcategory.sla_hours)
                
                # Добавляем запись в историю
                history = IncidentHistory(
                    incident_id=incident.id,
                    changed_by=session.get('user_id', 1),
                    field_name='status',
                    old_value=None,
                    new_value='new',
                    change_reason='Инцидент создан'
                )
                db.session.add(history)
                db.session.commit()
                
                flash(f'Инцидент {incident.incident_number} создан успешно!', 'success')
                return redirect(url_for('incidents'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при создании инцидента: {str(e)}', 'error')
    
    return render_template('create_incident.html', 
                         form=form, 
                         stores=stores, 
                         categories=categories, 
                         users=users)

@app.route('/api/subcategories/<int:category_id>')
@login_required
def get_subcategories(category_id):
    """API для получения подкатегорий по категории"""
    subcategories = IncidentSubcategory.query.filter_by(
        category_id=category_id, 
        is_active=True
    ).all()
    
    return jsonify([{
        'id': sub.id,
        'name': sub.name,
        'sla_hours': sub.sla_hours
    } for sub in subcategories])

@app.route('/api/departments/<int:store_id>')
@login_required
def get_departments(store_id):
    """API для получения отделов по магазину"""
    store = Store.query.get_or_404(store_id)
    departments = store.departments.all()  # Убираем фильтр is_active
    
    return jsonify([{
        'id': dept.id,
        'name': dept.name,
        'floor_number': dept.floor_number
    } for dept in departments])

@app.route('/incidents/<int:incident_id>')
@login_required
def view_incident(incident_id):
    """Просмотр детальной информации об инциденте"""
    incident = Incident.query.get_or_404(incident_id)
    comments = IncidentComment.query.filter_by(incident_id=incident_id).order_by(IncidentComment.created_at.desc()).all()
    history = IncidentHistory.query.filter_by(incident_id=incident_id).order_by(IncidentHistory.created_at.desc()).all()
    
    return render_template('view_incident.html', 
                         incident=incident, 
                         comments=comments, 
                         history=history)

@app.route('/acts')
@login_required
def acts():
    return render_template('acts.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/kpi')
@login_required
def kpi():
    return render_template('kpi.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.form)
        
        if form.validate():
            flash('Сообщение отправлено успешно!', 'success')
            return redirect(url_for('index'))
    
    return render_template('contact.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)