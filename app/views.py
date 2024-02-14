from flask import render_template

# Main page view
# display the users
class Homepage:
    def __init__(self, template_name='index.html'):
        self.template_name = template_name

    def render(self, users):
        return render_template(self.template_name, users=users)