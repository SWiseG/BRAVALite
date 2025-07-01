# core/django_tables.py
# -*- coding: utf-8 -*-
"""
Customização das tabelas padrão do Django para UPPERCASE
"""
from django.db import migrations, models

# Não é possível alterar diretamente as tabelas do Django
# Mas podemos criar proxy models ou usar database_forward para renomear

# Alternativa: Usar migrations customizadas
class Migration(migrations.Migration):
    """Migration customizada para renomear tabelas Django"""
    
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('sessions', '0001_initial'),
    ]
    
    operations = [
        # Renomear tabelas padrão do Django
        migrations.RunSQL(
            "ALTER TABLE auth_group RENAME TO AUTH_GROUP;",
            reverse_sql="ALTER TABLE AUTH_GROUP RENAME TO auth_group;"
        ),
        migrations.RunSQL(
            "ALTER TABLE auth_group_permissions RENAME TO AUTH_GROUP_PERMISSIONS;",
            reverse_sql="ALTER TABLE AUTH_GROUP_PERMISSIONS RENAME TO auth_group_permissions;"
        ),
        migrations.RunSQL(
            "ALTER TABLE auth_permission RENAME TO AUTH_PERMISSION;",
            reverse_sql="ALTER TABLE AUTH_PERMISSION RENAME TO auth_permission;"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_admin_log RENAME TO DJANGO_ADMIN_LOG;",
            reverse_sql="ALTER TABLE DJANGO_ADMIN_LOG RENAME TO django_admin_log;"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_content_type RENAME TO DJANGO_CONTENT_TYPE;",
            reverse_sql="ALTER TABLE DJANGO_CONTENT_TYPE RENAME TO django_content_type;"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_migrations RENAME TO DJANGO_MIGRATIONS;",
            reverse_sql="ALTER TABLE DJANGO_MIGRATIONS RENAME TO django_migrations;"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_session RENAME TO DJANGO_SESSION;",
            reverse_sql="ALTER TABLE DJANGO_SESSION RENAME TO django_session;"
        ),
        
        # Renomear colunas para UPPERCASE (exemplo para auth_permission)
        migrations.RunSQL(
            """
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN id TO ID;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN name TO NAME;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN content_type_id TO CONTENT_TYPE_ID;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN codename TO CODENAME;
            """,
            reverse_sql="""
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN ID TO id;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN NAME TO name;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN CONTENT_TYPE_ID TO content_type_id;
            ALTER TABLE AUTH_PERMISSION 
            RENAME COLUMN CODENAME TO codename;
            """
        ),
    ]
