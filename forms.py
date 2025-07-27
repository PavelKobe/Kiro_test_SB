# Простые формы без Flask-WTF для избежания конфликтов версий

class SimpleForm:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}
    
    def validate(self):
        return len(self.errors) == 0

class ContactForm(SimpleForm):
    def __init__(self, data=None):
        super().__init__(data)
        self.name = self.data.get('name', '')
        self.email = self.data.get('email', '')
        self.message = self.data.get('message', '')
    
    def validate(self):
        self.errors = {}
        
        if not self.name or len(self.name) < 2:
            self.errors['name'] = 'Имя должно содержать минимум 2 символа'
        
        if not self.email or '@' not in self.email:
            self.errors['email'] = 'Введите корректный email'
        
        if not self.message or len(self.message) < 10:
            self.errors['message'] = 'Сообщение должно содержать минимум 10 символов'
        
        return len(self.errors) == 0

class LoginForm(SimpleForm):
    def __init__(self, data=None):
        super().__init__(data)
        self.username = self.data.get('username', '')
        self.password = self.data.get('password', '')
    
    def validate(self):
        self.errors = {}
        
        if not self.username:
            self.errors['username'] = 'Введите имя пользователя'
        
        if not self.password:
            self.errors['password'] = 'Введите пароль'
        
        return len(self.errors) == 0

class IncidentForm(SimpleForm):
    def __init__(self, data=None):
        super().__init__(data)
        self.title = self.data.get('title', '')
        self.description = self.data.get('description', '')
        self.category_id = self.data.get('category_id', '')
        self.subcategory_id = self.data.get('subcategory_id', '')
        self.priority = self.data.get('priority', 'medium')
        self.severity = self.data.get('severity', 'minor')
        self.store_id = self.data.get('store_id', '')
        self.department_id = self.data.get('department_id', '')
        self.location_details = self.data.get('location_details', '')
        self.assigned_to = self.data.get('assigned_to', '')
        self.customer_affected = self.data.get('customer_affected', 'false')
    
    def validate(self):
        self.errors = {}
        
        if not self.title or len(self.title) < 5:
            self.errors['title'] = 'Заголовок должен содержать минимум 5 символов'
        
        if len(self.title) > 200:
            self.errors['title'] = 'Заголовок не должен превышать 200 символов'
        
        if not self.description or len(self.description) < 10:
            self.errors['description'] = 'Описание должно содержать минимум 10 символов'
        
        if not self.category_id:
            self.errors['category_id'] = 'Выберите категорию инцидента'
        
        if not self.store_id:
            self.errors['store_id'] = 'Выберите магазин'
        
        if self.priority not in ['low', 'medium', 'high', 'critical']:
            self.errors['priority'] = 'Некорректный приоритет'
        
        if self.severity not in ['minor', 'major', 'critical']:
            self.errors['severity'] = 'Некорректная серьезность'
        
        return len(self.errors) == 0