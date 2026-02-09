"""Script pour adapter le dashboard Timbrage existant au projet Flask"""
import re

# Lire le fichier original
with open(r'app\templates\dashboard\timbrage_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire le CSS
css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
css_content = css_match.group(1) if css_match else ''

# Extraire le body content
body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
body_content = body_match.group(1) if body_match else content

# Supprimer les balises main si elles existent
body_content = re.sub(r'<main[^>]*>', '', body_content)
body_content = re.sub(r'</main>', '', body_content)

# Extraire le JavaScript
script_match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
script_content = script_match.group(1) if script_match else ''

# Remplacer le nom codé en dur
body_content = body_content.replace('Hedia', '{{ current_user.username }}')
body_content = body_content.replace('/api/dashboard', '/dashboard/api/timbrage/data')

# Créer le nouveau template
template_parts = []
template_parts.append('{{% extends "base.html" %}}\n\n')
template_parts.append('{{% block title %}}Dashboard Timbrage - E-Trans{{% endblock %}}\n\n')
template_parts.append('{{% block css %}}\n<style>\n')
template_parts.append(css_content)
template_parts.append('\n</style>\n{{% endblock %}}\n\n')
template_parts.append('{{% block content %}}\n')
template_parts.append(body_content)
template_parts.append('\n{{% endblock %}}\n\n')
template_parts.append('{{% block scripts %}}\n<script>\n')
template_parts.append(script_content)
template_parts.append('\n</script>\n{{% endblock %}}\n')

new_template = ''.join(template_parts)

# Écrire le nouveau fichier
with open(r'app\templates\dashboard\timbrage_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(new_template)

print("✓ Dashboard Timbrage adapté avec succès!")
