"""
Модели SQLAlchemy для системы управления инцидентами торговой сети Stockmann
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func, text
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    cities = db.relationship('City', backref='country', lazy=True)
    
    def __repr__(self):
        return f'<Country {self.code}: {self.name}>'

class City(db.Model):
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    stores = db.relationship('Store', backref='city', lazy=True)
    
    def __repr__(self):
        return f'<City {self.name}, {self.country.name}>'

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    store_type = db.Column(db.String(50), nullable=False)  # department_store, outlet, online
    area_sqm = db.Column(db.Integer)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    manager_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    opened_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    users = db.relationship('User', backref='store', lazy=True)
    incidents = db.relationship('Incident', backref='store', lazy=True)
    work_shifts = db.relationship('WorkShift', backref='store', lazy=True)
    
    # Многие ко многим с отделами
    departments = db.relationship('Department', secondary='store_departments', 
                                back_populates='stores', lazy='dynamic')
    
    @hybrid_property
    def active_incidents_count(self):
        return len([i for i in self.incidents if i.status not in ['closed', 'cancelled']])
    
    def __repr__(self):
        return f'<Store {self.code}: {self.name}>'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    floor_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    incidents = db.relationship('Incident', backref='department', lazy=True)
    
    # Многие ко многим с магазинами
    stores = db.relationship('Store', secondary='store_departments', 
                           back_populates='departments', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'

class StoreDepartment(db.Model):
    __tablename__ = 'store_departments'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    __table_args__ = (db.UniqueConstraint('store_id', 'department_id'),)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    position = db.Column(db.String(100))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    role = db.Column(db.String(50), nullable=False, default='user')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    reported_incidents = db.relationship('Incident', foreign_keys='Incident.reporter_id', 
                                       backref='reporter', lazy=True)
    assigned_incidents = db.relationship('Incident', foreign_keys='Incident.assigned_to', 
                                       backref='assignee', lazy=True)
    resolved_incidents = db.relationship('Incident', foreign_keys='Incident.resolver_id', 
                                       backref='resolver', lazy=True)
    
    @hybrid_property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @hybrid_property
    def active_assigned_count(self):
        return len([i for i in self.assigned_incidents if i.status not in ['closed', 'cancelled']])
    
    def __repr__(self):
        return f'<User {self.username}: {self.full_name}>'

class IncidentCategory(db.Model):
    __tablename__ = 'incident_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7))  # HEX color
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    subcategories = db.relationship('IncidentSubcategory', backref='category', lazy=True)
    incidents = db.relationship('Incident', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<IncidentCategory {self.code}: {self.name}>'

class IncidentSubcategory(db.Model):
    __tablename__ = 'incident_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('incident_categories.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sla_hours = db.Column(db.Integer, default=24)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    incidents = db.relationship('Incident', backref='subcategory', lazy=True)
    
    def __repr__(self):
        return f'<IncidentSubcategory {self.code}: {self.name}>'

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Классификация
    category_id = db.Column(db.Integer, db.ForeignKey('incident_categories.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('incident_subcategories.id'))
    priority = db.Column(db.String(20), nullable=False, default='medium')
    severity = db.Column(db.String(20), nullable=False, default='minor')
    
    # Локация
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    location_details = db.Column(db.Text)
    
    # Статус и временные метки
    status = db.Column(db.String(30), nullable=False, default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    
    # Участники
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Дополнительная информация
    customer_affected = db.Column(db.Boolean, default=False)
    financial_impact = db.Column(db.Numeric(10, 2))
    resolution_notes = db.Column(db.Text)
    
    # SLA
    sla_deadline = db.Column(db.DateTime)
    sla_breached = db.Column(db.Boolean, default=False)
    
    # Метаданные
    source = db.Column(db.String(50), default='manual')
    external_ticket_id = db.Column(db.String(100))
    
    # Отношения
    history = db.relationship('IncidentHistory', backref='incident', lazy=True, 
                            cascade='all, delete-orphan')
    comments = db.relationship('IncidentComment', backref='incident', lazy=True,
                             cascade='all, delete-orphan')
    attachments = db.relationship('IncidentAttachment', backref='incident', lazy=True,
                                cascade='all, delete-orphan')
    escalations = db.relationship('IncidentEscalation', backref='incident', lazy=True,
                                cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='incident', lazy=True,
                                  cascade='all, delete-orphan')
    
    @hybrid_property
    def is_overdue(self):
        if self.sla_deadline and self.status not in ['resolved', 'closed', 'cancelled']:
            return datetime.utcnow() > self.sla_deadline
        return False
    
    @hybrid_property
    def age_hours(self):
        return (datetime.utcnow() - self.created_at).total_seconds() / 3600
    
    @hybrid_property
    def resolution_time_hours(self):
        if self.resolved_at:
            return (self.resolved_at - self.created_at).total_seconds() / 3600
        return None
    
    def __repr__(self):
        return f'<Incident {self.incident_number}: {self.title}>'

class IncidentHistory(db.Model):
    __tablename__ = 'incident_history'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    change_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    user = db.relationship('User', backref='incident_changes', lazy=True)
    
    def __repr__(self):
        return f'<IncidentHistory {self.incident_id}: {self.field_name}>'

class IncidentComment(db.Model):
    __tablename__ = 'incident_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_text = db.Column(db.Text, nullable=False)
    is_internal = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    user = db.relationship('User', backref='comments', lazy=True)
    
    def __repr__(self):
        return f'<IncidentComment {self.incident_id}: {self.user.username if self.user else "System"}>'

class IncidentAttachment(db.Model):
    __tablename__ = 'incident_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    uploader = db.relationship('User', backref='uploaded_files', lazy=True)
    
    def __repr__(self):
        return f'<IncidentAttachment {self.original_filename}>'

class IncidentRelation(db.Model):
    __tablename__ = 'incident_relations'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    child_incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    relation_type = db.Column(db.String(20), nullable=False)  # duplicate, related, blocks, caused_by
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    parent_incident = db.relationship('Incident', foreign_keys=[parent_incident_id], 
                                    backref='child_relations', lazy=True)
    child_incident = db.relationship('Incident', foreign_keys=[child_incident_id], 
                                   backref='parent_relations', lazy=True)
    creator = db.relationship('User', backref='created_relations', lazy=True)
    
    __table_args__ = (
        db.CheckConstraint('parent_incident_id != child_incident_id', 
                          name='chk_not_self_related'),
    )
    
    def __repr__(self):
        return f'<IncidentRelation {self.parent_incident_id} -> {self.child_incident_id}: {self.relation_type}>'

class IncidentEscalation(db.Model):
    __tablename__ = 'incident_escalations'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    escalated_from = db.Column(db.Integer, db.ForeignKey('users.id'))
    escalated_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    escalation_level = db.Column(db.Integer, nullable=False, default=1)
    reason = db.Column(db.Text, nullable=False)
    escalated_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Отношения
    from_user = db.relationship('User', foreign_keys=[escalated_from], 
                              backref='escalations_from', lazy=True)
    to_user = db.relationship('User', foreign_keys=[escalated_to], 
                            backref='escalations_to', lazy=True)
    
    def __repr__(self):
        return f'<IncidentEscalation {self.incident_id}: Level {self.escalation_level}>'

class SLARule(db.Model):
    __tablename__ = 'sla_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('incident_categories.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('incident_subcategories.id'))
    priority = db.Column(db.String(20))
    severity = db.Column(db.String(20))
    response_time_hours = db.Column(db.Integer, nullable=False)
    resolution_time_hours = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    category = db.relationship('IncidentCategory', backref='sla_rules', lazy=True)
    subcategory = db.relationship('IncidentSubcategory', backref='sla_rules', lazy=True)
    
    def __repr__(self):
        return f'<SLARule {self.category.code if self.category else "ALL"}: {self.resolution_time_hours}h>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # email, sms, push, system
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    user = db.relationship('User', backref='notifications', lazy=True)
    
    def __repr__(self):
        return f'<Notification {self.notification_type}: {self.subject}>'

class WorkShift(db.Model):
    __tablename__ = 'work_shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    shift_name = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<WorkShift {self.store.code}: {self.shift_name}>'

# Вспомогательные функции для работы с моделями

def get_incident_stats_by_store(store_id=None):
    """Получить статистику инцидентов по магазину"""
    query = db.session.query(
        Incident.status,
        func.count(Incident.id).label('count')
    )
    
    if store_id:
        query = query.filter(Incident.store_id == store_id)
    
    return query.group_by(Incident.status).all()

def get_overdue_incidents(store_id=None):
    """Получить просроченные инциденты"""
    query = db.session.query(Incident).filter(
        Incident.sla_deadline < datetime.utcnow(),
        Incident.status.notin_(['resolved', 'closed', 'cancelled'])
    )
    
    if store_id:
        query = query.filter(Incident.store_id == store_id)
    
    return query.all()

def get_user_workload(user_id):
    """Получить рабочую нагрузку пользователя"""
    return db.session.query(
        Incident.status,
        func.count(Incident.id).label('count')
    ).filter(
        Incident.assigned_to == user_id,
        Incident.status.notin_(['closed', 'cancelled'])
    ).group_by(Incident.status).all()